# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.core import cfg
from telegram_bot.keyboards import create_admin_inline
from telegram_bot.utils import edit_message


router = Router()


# Колбэк получения списка карт
@router.callback_query(StateFilter('*'), F.data == "admin", F.from_user.id.in_(cfg.ADMIN_IDS))
async def admin_menu_callback_run(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    try:
        keyboard = await create_admin_inline()

        await edit_message(
            message=callback_query.message,
            text=cfg.MAIN_ADMIN_TEXT,
            keyboard=keyboard,
            media=f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_ADMIN_PHOTO}"
        )
        text_answer = "Админ режим"

    except:
        text_answer = "Ошибка админ режима"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )
