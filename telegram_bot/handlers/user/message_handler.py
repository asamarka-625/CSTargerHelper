# Внешние зависимости
from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.keyboards import create_main_inline
from telegram_bot.core import cfg
from telegram_bot.crud import sql_add_or_update_user


router = Router()


# Стартовая команда
@router.message(StateFilter('*'), Command('start'))
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await sql_add_or_update_user(
        telegram_id=message.from_user.id,
        telegram_username=message.from_user.username,
        telegram_first_name=message.from_user.first_name,
        telegram_last_name=message.from_user.last_name
    )
    
    await message.answer_photo(
        photo=FSInputFile(f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"),
        caption=cfg.MAIN_USER_TEXT,
        reply_markup=create_main_inline(user_id=message.from_user.id)
    )


