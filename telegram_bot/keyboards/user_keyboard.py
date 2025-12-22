# Внешние зависимости
from typing import Optional, List
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# Внутренние модули
from telegram_bot.core import cfg
from telegram_bot.crud import (sql_get_all_maps, sql_get_categories_by_map, sql_get_cards_by_category,
                               sql_get_card_image_by_id)
from models import CardImage


# Создаем инлайн кнопки (главное меню)
async def create_main_inline(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎮 Карты", callback_data="maps"))

    if user_id in cfg.ADMIN_IDS:
        builder.row(InlineKeyboardButton(text="👑 Админ", callback_data="admin"))

    return builder.as_markup()


# Создаем инлайн кнопки профиля
async def create_profile_inline(hash_user_data: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Обновить", callback_data=f"upd_profile:{hash_user_data}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back main"))
    
    return builder.as_markup()
    

# Создаем инлайн кнопки (доступные карты)
async def create_maps_inline(admin: bool = False):
    builder = InlineKeyboardBuilder()

    maps = await sql_get_all_maps()

    if not admin:
        tag = "map"
        back = "back main"

    else:
        tag = "admin_map"
        back = "back admin"

    if maps:
        text = "Выберите карту из списка"
        for i in range(0, len(maps), 2):
            if (i + 1) < len(maps):
                builder.row(
                    InlineKeyboardButton(
                        text=maps[i].name.upper(),
                        callback_data=f"{tag}:{maps[i].id}"
                    ),
                    InlineKeyboardButton(
                        text=maps[i+1].name.upper(),
                        callback_data=f"{tag}:{maps[i+1].id}"
                    ),
                )
            else:
                builder.row(
                    InlineKeyboardButton(
                        text=maps[i].name.upper(),
                        callback_data=f"{tag}:{maps[i].id}"
                    )
                )

    else:
       text = "Нет доступных карт"

    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=back))

    return text, builder.as_markup()



# Создаем инлайн кнопки (категории для выбранной карты)
async def create_categories_inline(map_id: int, admin: bool = False):
    builder = InlineKeyboardBuilder()

    categories = await sql_get_categories_by_map(map_id=map_id)

    if not admin:
        tag = "category"
        back = "back map"

    else:
        tag = "admin_category"
        back = "back admin"

    if categories:
        text = "Выберите категорию из списка"
        for i in range(0, len(categories), 2):
            if (i + 1) < len(categories):
                builder.row(
                    InlineKeyboardButton(
                        text=categories[i].name.upper(),
                        callback_data=f"{tag}:{map_id}:{categories[i].id}"
                    ),
                    InlineKeyboardButton(
                        text=categories[i+1].name.upper(),
                        callback_data=f"{tag}:{map_id}:{categories[i+1].id}"
                    ),
                )
            else:
                builder.row(
                    InlineKeyboardButton(
                        text=categories[i].name.upper(),
                        callback_data=f"{tag}:{map_id}:{categories[i].id}"
                    )
                )

    else:
        text = "Нет доступных категорий"

    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=back))

    return text, builder.as_markup()


# Создаем инлайн кнопки (карточки для выбранной категории)
async def create_cards_inline(map_id: int, category_id: int):
    builder = InlineKeyboardBuilder()

    cards = await sql_get_cards_by_category(category_id=category_id)

    if cards:
        text = "Выберите карточку из списка"
        for i in range(0, len(cards), 2):
            if (i + 1) < len(cards):
                builder.row(
                    InlineKeyboardButton(
                        text=cards[i].name.upper(),
                        callback_data=f"card:{map_id}:{category_id}:{cards[i].id}"
                    ),
                    InlineKeyboardButton(
                        text=cards[i+1].name.upper(),
                        callback_data=f"card:{map_id}:{category_id}:{cards[i+1].id}"
                    ),
                )
            else:
                builder.row(
                    InlineKeyboardButton(
                        text=cards[i].name.upper(),
                        callback_data=f"card:{map_id}:{category_id}:{cards[i].id}"
                    )
                )

    else:
        text = "Нет доступных карточек"

    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"back category:{map_id}"))

    return text, builder.as_markup()


# Создаем инлайн кнопки просмотра изображений карточки
async def create_card_images_inline(
    map_id: int,
    category_id: int,
    card_id: int,
    order: int,
    images: Optional[List[CardImage]] = None
):
    if images is None:
        prev_image, next_image, image = await sql_get_card_image_by_id(
            card_id=card_id,
            order=order
        )

    else:
        image = next((image for i, image in enumerate(images) if image.order == order), None)
        prev_image, next_image = False, image.order < len(images)

    builder = InlineKeyboardBuilder()
    navigation = []

    if prev_image:
        navigation.append(InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=f"image:{map_id}:{category_id}:{card_id}:{order-1}")
        )

    if next_image:
        navigation.append(InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=f"image:{map_id}:{category_id}:{card_id}:{order+1}")
        )

    builder.row(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data=f"back cards:{map_id}:{category_id}")
    )

    return image, builder.as_markup()