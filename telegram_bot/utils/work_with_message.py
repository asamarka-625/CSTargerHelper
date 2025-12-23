# Внешние зависимости
from typing import Optional
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def edit_message(
    message: Message,
    text: Optional[str] = None,
    keyboard: Optional[InlineKeyboardBuilder] = None,
    media: Optional[str] = None
):
    add_kwargs = {}

    if text is None:
        text = message.caption

    if keyboard is None:
        add_kwargs['reply_markup'] = message.reply_markup

    else:
        add_kwargs['reply_markup'] = keyboard

    if media is not None:
        add_kwargs["media"] = InputMediaPhoto(
            media=FSInputFile(media),
            caption=text
        )
        await message.edit_media(**add_kwargs)

    else:
        await message.edit_caption(caption=text, **add_kwargs)