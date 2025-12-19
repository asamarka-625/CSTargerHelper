# Внешние зависимости
from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.keyboards import create_main_inline
from telegram_bot.core import cfg


router = Router()


# Стартовая команда
@router.message(StateFilter('*'), Command('start'))
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    await message.answer_photo(
        photo=FSInputFile(f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"),
        caption=cfg.MAIN_USER_TEXT,
        reply_markup=await create_main_inline(user_id=message.from_user.id)
    )


