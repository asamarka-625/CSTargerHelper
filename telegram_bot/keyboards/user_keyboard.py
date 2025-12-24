# Внешние зависимости
from typing import Sequence, Optional, List
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# Внутренние модули
from telegram_bot.core import cfg
from telegram_bot.crud import (sql_get_all_maps, sql_get_categories_by_map, sql_get_cards_by_category,
                               sql_get_card_image_by_id)
from models import CardImage


# Вспомогательная функция для создания страницы
def create_page(
    obj: Sequence,
    prev_page: bool,
    next_page: bool,
    offset: int,
    tag: str,
    back: str
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for i in range(0, len(obj), 2):
        id_num = i + offset
        if (i + 1) < len(obj):
            builder.row(
                InlineKeyboardButton(
                    text=f"{id_num}) {obj[i][1].upper()}",
                    callback_data=f"{tag}:{obj[i][0]}"
                ),
                InlineKeyboardButton(
                    text=f"{id_num+1}) {obj[i+1][1].upper()}",
                    callback_data=f"{tag}:{obj[i + 1][0]}"
                ),
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text=f"{id_num}) {obj[i][1].upper()}",
                    callback_data=f"{tag}:{obj[i][0]}"
                )
            )

    page = offset // cfg.LIMIT_VIEW_PAGE
    navigation = []

    if prev_page:
        navigation.append(InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=f"prev {tag}:{page}"
        ))

    if next_page:
        navigation.append(InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=f"next {tag}:{page}"
        ))

    if navigation:
        builder.row(*navigation)

    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"back {back}"))

    return builder


# Вспомогательная функция для создания текста на странице
def create_text_on_page(
    obj: Sequence,
    offset: int,
    text_for_exists: str,
    text_for_no_exists: str
) -> str:
    text = f"{text_for_exists}\n\n"
    if obj:
        for i in range(0, len(obj), 2):
            id_num = i + offset
            if (i + 1) < len(obj):
                text += f"{id_num}) {obj[i][1].upper()}           {id_num+1}) {obj[i+1][1].upper()}\n"
            else:
                text += f"{id_num}) {obj[i][1].upper()}"

        return text

    else:
        return text_for_no_exists


# Создаем инлайн кнопки (главное меню)
def create_main_inline(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎮 Карты", callback_data="maps"))
    builder.row(
        InlineKeyboardButton(text="📚 Мои карточки", callback_data="my_maps"),
        InlineKeyboardButton(text="❤️ Избранное", callback_data="favorites")
    )
    builder.row(
        InlineKeyboardButton(text="🔎 Поиск карточки", callback_data="search"),
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
    )

    if user_id in cfg.ADMIN_IDS:
        builder.row(InlineKeyboardButton(text="👑 Админ", callback_data="admin"))

    return builder.as_markup()


# Создаем инлайн кнопки профиля
def create_profile_inline(hash_user_data: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="♻️ Обновить", callback_data=f"upd_profile:{hash_user_data}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back main"))
    
    return builder.as_markup()
    

# Создаем инлайн кнопки (доступные карты)
async def create_maps_inline(
    admin: bool = False,
    offset: int = 0
):
    prev_page, next_page, maps = await sql_get_all_maps(offset=offset)

    if not admin:
        tag = "map"
        back = "main"

    else:
        tag = "map-admin"
        back = "admin"


    text = create_text_on_page(
        obj=maps,
        offset=offset,
        text_for_exists="Выберите карту из списка",
        text_for_no_exists="Нет доступных карт"
    )

    builder = create_page(
        obj=maps,
        prev_page=prev_page,
        next_page=next_page,
        offset=offset,
        tag=tag,
        back=back
    )

    return text, builder.as_markup()


# Создаем инлайн кнопки (категории для выбранной карты)
async def create_categories_inline(
    map_id: int,
    admin: bool = False,
    offset: int = 0
):
    prev_page, next_page, categories = await sql_get_categories_by_map(
        map_id=map_id,
        offset=offset
    )

    if not admin:
        tag = f"category:{map_id}"
        back = "map"

    else:
        tag = f"category-admin:{map_id}"
        back = "admin"

    text = create_text_on_page(
        obj=categories,
        offset=offset,
        text_for_exists="Выберите категорию из списка",
        text_for_no_exists="Нет доступных категорий"
    )

    builder = create_page(
        obj=categories,
        prev_page=prev_page,
        next_page=next_page,
        offset=offset,
        tag=tag,
        back=back
    )

    return text, builder.as_markup()


# Создаем инлайн кнопки (карточки для выбранной категории)
async def create_cards_inline(
    map_id: int,
    category_id: int,
    offset: int = 0
):
    prev_page, next_page, cards = await sql_get_cards_by_category(
        category_id=category_id,
        offset=offset
    )

    text = create_text_on_page(
        obj=cards,
        offset=offset,
        text_for_exists="Выберите карточку из списка",
        text_for_no_exists="Нет доступных карточек"
    )

    builder = create_page(
        obj=cards,
        prev_page=prev_page,
        next_page=next_page,
        offset=offset,
        tag=f"card:{map_id}:{category_id}",
        back=f"category:{map_id}"
    )

    return text, builder.as_markup()


# Создаем инлайн кнопки просмотра изображений карточки
async def create_card_images_inline(
    map_id: int,
    category_id: int,
    card_id: int,
    order: int,
    user_favorite: int,
    share_link: str,
    max_image: Optional[int] = None,
    images: Optional[List[CardImage]] = None
):
    if max_image is None:
        max_image = len(images)

    if images is None:
        image = await sql_get_card_image_by_id(
            card_id=card_id,
            order=order
        )
        prev_image, next_image = image.order > 1, image.order < max_image

    else:
        image = next((image for i, image in enumerate(images) if image.order == order), None)
        prev_image, next_image = False, order > 1


    navigation = []
    if prev_image:
        navigation.append(InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=f"image:{user_favorite}:{map_id}:{category_id}:{card_id}:{max_image}:{order-1}")
        )

    if next_image:
        navigation.append(InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=f"image:{user_favorite}:{map_id}:{category_id}:{card_id}:{max_image}:{order+1}")
        )

    builder = InlineKeyboardBuilder()
    if navigation:
        builder.row(*navigation)

    builder.row(
        InlineKeyboardButton(
            text="💔 Убрать из избранного" if user_favorite else "❤️ В избранное",
            callback_data=f"favorite:{user_favorite}:{map_id}:{category_id}:{card_id}:{max_image}:{order}"
        ),
        InlineKeyboardButton(
            text="↪ Поделиться",
            url=share_link
        )
    )

    builder.row(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data=f"back cards:{map_id}:{category_id}")
    )

    return image.file_name, builder.as_markup()


# Создаем инлайн кнопку назад
async def create_back_inline(back: str):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data=f"back {back}")
    )

    return builder.as_markup()


# Создаем инлайн кнопку главное меню
async def create_main_menu_inline():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="🔙 Главное меню",
        callback_data="main")
    )

    return builder.as_markup()