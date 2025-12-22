# Внешние зависимости
import uuid
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.core import cfg
from telegram_bot.keyboards import create_maps_inline, create_admin_inline, create_categories_inline
from telegram_bot.utils import edit_message
from telegram_bot.crud import sql_add_card, sql_add_card_image


# Состояние для добавления карточки
class AddCard(StatesGroup):
    state_map = State()
    state_category = State()
    state_card_name = State()
    state_card_description = State()
    state_card_images = State()


router = Router()


# Колбэк добавления карточки
@router.callback_query(F.data == "add card", F.from_user.id.in_(cfg.ADMIN_IDS))
async def admin_add_card_callback_run(callback_query: CallbackQuery, state: FSMContext):
    try:
        text, keyboard = await create_maps_inline(admin=True)

        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard
        )
        text_answer = "Выберите карту"
        await state.set_state(AddCard.state_map)

    except:
        text_answer = "Ошибка добавления новой категории"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк выбора карты для добавления карточки
@router.callback_query(
    AddCard.state_map,
    F.data.startswith("admin_map:"),
    F.from_user.id.in_(cfg.ADMIN_IDS)
)
async def admin_add_card_choice_map_callback_run(callback_query: CallbackQuery, state: FSMContext):
    map_id = int(callback_query.data.replace("admin_map:", ""))

    try:
        text, keyboard = await create_categories_inline(map_id=map_id, admin=True)

        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard
        )
        text_answer = "Выберите категорию"
        await state.set_state(AddCard.state_category)

    except:
        text_answer = "Ошибка выбора карты"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк выбора категории для добавления карточки
@router.callback_query(
    AddCard.state_category,
    F.data.startswith("admin_category:"),
    F.from_user.id.in_(cfg.ADMIN_IDS)
)
async def admin_add_card_choice_category_callback_run(callback_query: CallbackQuery, state: FSMContext):
    map_category_id = callback_query.data.replace("admin_category:", "")
    _, category_id = map(int, map_category_id.split(":"))

    await state.update_data(category_id=category_id)

    try:
        await edit_message(
            message=callback_query.message,
            text="Напишите название новой карточки",
        )
        text_answer = "Напишите название новой карточки"
        await state.set_state(AddCard.state_card_name)

    except:
        text_answer = "Ошибка выбора категории"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Добавление названия новой карточки
@router.message(AddCard.state_card_name, F.from_user.id.in_(cfg.ADMIN_IDS))
async def add_card_name(message: Message, state: FSMContext):
    card_name = message.text.strip()

    await state.update_data(name=card_name)
    await state.set_state(AddCard.state_card_description)

    await message.answer(
        text=f"Название '{card_name}' успешно записано!\nНапишите описание для карточки"
    )

# Добавление описания новой карточки
@router.message(AddCard.state_card_description, F.from_user.id.in_(cfg.ADMIN_IDS))
async def add_card_description(message: Message, state: FSMContext):
    card_description = message.text.strip()

    await state.update_data(description=card_description)
    await state.set_state(AddCard.state_card_images)

    await message.answer(
        text=f"Описание '{card_description}' успешно записано!\nПришлите изображения для карточки"
    )


# Добавление изображений и создания карточки
@router.message(
    AddCard.state_card_images,
    F.photo,
    F.from_user.id.in_(cfg.ADMIN_IDS)
)
async def add_card_images(message: Message, state: FSMContext, bot: Bot):
    photos = message.photo
    data = await state.get_data()

    card_id = await sql_add_card(
        name=data["name"],
        description=data["description"],
        category_id=data["category_id"]
    )

    for i, photo in enumerate(photos, 1):
        # Скачиваем фото
        file_info = await bot.get_file(photo[-1].file_id)
        file_name = f"{uuid.uuid4()}.jpg"

        await bot.download_file(file_info.file_path, f"{cfg.IMAGES_DIR}/cards/{file_name}")

        await sql_add_card_image(
            file_name=file_name,
            order=i,
            card_id=card_id
        )

    await state.clear()

    await message.answer(
        text=f"Новая карточка '{data["name"]}' успешно добавлена!",
        reply_markup=await create_admin_inline()
    )