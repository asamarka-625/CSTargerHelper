# Внешние зависимости
import uuid
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.core import cfg
from telegram_bot.keyboards import create_admin_inline
from telegram_bot.utils import edit_message
from telegram_bot.crud import sql_add_map


# Состояние для добавления карты
class AddMap(StatesGroup):
    state_map_name = State()
    state_map_image = State()


router = Router()


# Колбэк добавления карты
@router.callback_query(F.data == "add map", F.from_user.id.in_(cfg.ADMIN_IDS))
async def admin_add_map_callback_run(callback_query: CallbackQuery, state: FSMContext):
    try:
        await edit_message(
            message=callback_query.message,
            text="Напишите название новой карты",
        )
        text_answer = "Напишите название новой карты"
        await state.set_state(AddMap.state_map_name)

    except:
        text_answer = "Ошибка добавления новой карты"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Добавление названия новой карты
@router.message(AddMap.state_map_name, F.from_user.id.in_(cfg.ADMIN_IDS))
async def admin_add_map_name(message: Message, state: FSMContext):
    map_name = message.text.strip()

    await state.update_data(name=map_name)
    await state.set_state(AddMap.state_map_image)

    await message.answer(
        text=f"Имя '{map_name}' успешно записано!\nПришлите изображение новой карты"
    )


# Добавление изображения карты
@router.message(
    AddMap.state_map_image,
    F.photo,
    F.from_user.id.in_(cfg.ADMIN_IDS)
)
async def admin_add_map_image(message: Message, state: FSMContext, bot: Bot):
    photos = message.photo

    data = await state.get_data()

    file_info = await bot.get_file(photos[-1].file_id)
    file_name = f"{uuid.uuid4()}.jpg"

    await bot.download_file(file_info.file_path, f"{cfg.IMAGES_DIR}/maps/{file_name}")

    await sql_add_map(
        name=data["name"],
        image=file_name
    )
    await state.clear()

    await message.answer(
        text=f"Новая карта '{data["name"]}' успешно добавлена!",
        reply_markup=await create_admin_inline()
    )