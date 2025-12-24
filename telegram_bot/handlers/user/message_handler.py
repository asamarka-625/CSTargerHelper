# Внешние зависимости
from aiogram import Router
from aiogram.filters import StateFilter, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
# Внутренние модули
from telegram_bot.keyboards import create_main_inline, create_card_images_inline
from telegram_bot.core import cfg
from telegram_bot.crud import (sql_add_or_update_user, sql_get_card_by_number, sql_chek_favorite_card_for_user)


router = Router()


# Стартовая команда
@router.message(StateFilter('*'), CommandStart())
async def start_command(message: Message, state: FSMContext, command: CommandObject = None):
    await state.clear()

    await sql_add_or_update_user(
        telegram_id=message.from_user.id,
        telegram_username=message.from_user.username,
        telegram_first_name=message.from_user.first_name,
        telegram_last_name=message.from_user.last_name
    )

    card_number = None
    if command and command.args:
        try:
            # Ожидаем формат: start?card=number
            if "=" in command.args:
                card_number = command.args.split("=")[1]

        except:
            pass

    if card_number is not None:
        card = await sql_get_card_by_number(card_number=card_number)

        if card:
            user_favorite = await sql_chek_favorite_card_for_user(
                telegram_id=message.from_user.id,
                card_id=card.id
            )

            image, keyboard = await create_card_images_inline(
                map_id=card.map_id,
                category_id=card.category_id,
                card_id=card.id,
                order=len(card.images),
                user_favorite=user_favorite,
                images=card.images
            )

            text = (
                f"<b>Номер карточки: {card.card_number}</b>\n"
                f"<b>{card.name}</b>\n\n"
                f"Описание: {card.description}"
            )

            await message.answer_photo(
                photo=FSInputFile(f"{cfg.IMAGES_DIR}/cards/{image}"),
                caption=text,
                reply_markup=keyboard
            )
            return

    await message.answer_photo(
        photo=FSInputFile(f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"),
        caption=cfg.MAIN_USER_TEXT,
        reply_markup=create_main_inline(user_id=message.from_user.id)
    )


