# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.core import cfg
from telegram_bot.keyboards import create_maps_inline, create_admin_inline
from telegram_bot.utils import edit_message
from telegram_bot.crud import sql_add_category_for_map


# Состояние для добавления категории
class AddCategory(StatesGroup):
    state_map = State()
    state_category = State()


router = Router()


# Колбэк добавления категории
@router.callback_query(F.data == "add category", F.from_user.id.in_(cfg.ADMIN_IDS))
async def admin_add_category_callback_run(callback_query: CallbackQuery, state: FSMContext):
    try:
        keyboard = await create_maps_inline(admin=True)

        await edit_message(
            message=callback_query.message,
            text="Выберите карту, в которую нужно добавить категорию",
            keyboard=keyboard
        )
        text_answer = "Выберите карту"
        await state.set_state(AddCategory.state_map)

    except:
        text_answer = "Ошибка добавления новой категории"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк выбора карты для добавления категории
@router.callback_query(
    AddCategory.state_map,
    F.data.startswitch("admin_map:"),
    F.from_user.id.in_(cfg.ADMIN_IDS)
)
async def admin_add_category_choice_map_callback_run(callback_query: CallbackQuery, state: FSMContext):
    map_id = int(callback_query.data.replace("admin_map:", ""))
    await state.update_data(map_id=map_id)

    try:
        await edit_message(
            message=callback_query.message,
            text="Напишите название новой категории",
        )
        text_answer = "Напишите название новой категории"
        await state.set_state(AddCategory.state_category)

    except:
        text_answer = "Ошибка выбора карты"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Добавление новой категории
@router.message(AddCategory.state_category, F.from_user.id.in_(cfg.ADMIN_IDS))
async def add_category(message: Message, state: FSMContext):
    category_name = message.text.strip()
    data = await state.get_data()

    await sql_add_category_for_map(
        name=category_name,
        map_id=data["map_id"]
    )

    await state.clear()

    await message.answer(
        text=f"Новая категория '{category_name}' успешно добавлена!",
        reply_markup=await create_admin_inline()
    )