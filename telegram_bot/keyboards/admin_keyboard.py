# Внешние зависимости
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Создаем инлайн кнопки (админ меню)
async def create_admin_inline():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🗺️ Добавить карту", callback_data="add map"))
    builder.row(InlineKeyboardButton(text="📁 Добавить категорию", callback_data="add category"))
    builder.row(InlineKeyboardButton(text="🃏 Добавить карточку", callback_data="add card"))
    builder.row(InlineKeyboardButton(text="🔙 Главное меню", callback_data="back main"))

    return builder.as_markup()