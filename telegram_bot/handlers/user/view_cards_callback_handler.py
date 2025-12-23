# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery
# Внутренние модули
from telegram_bot.keyboards import (create_maps_inline, create_categories_inline, create_cards_inline,
                                    create_card_images_inline)
from telegram_bot.utils import edit_message
from telegram_bot.crud import sql_get_card_by_id, sql_get_map_image
from telegram_bot.core import cfg


router = Router()


# Колбэк получения списка карт
@router.callback_query(F.data == "maps")
async def get_map_callback_run(callback_query: CallbackQuery):
    try:
        text, keyboard = await create_maps_inline()

        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard
        )
        text_answer = "Выберите карту"

    except:
        text_answer = "Ошибка просмотра карт"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк выбора карты
@router.callback_query(F.data.startswith("map:"))
async def choice_map_callback_run(callback_query: CallbackQuery):
    map_id = int(callback_query.data.replace("map:", ""))

    try:
        text, keyboard = await create_categories_inline(map_id=map_id)
        map_image = await sql_get_map_image(map_id=map_id)

        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard,
            media=f"{cfg.IMAGES_DIR}/maps/{map_image}"
        )
        text_answer = "Выберите категорию"

    except:
        text_answer = "Ошибка выбора карты"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк выбора категории
@router.callback_query(F.data.startswith("category:"))
async def choice_category_callback_run(callback_query: CallbackQuery):
    map_category_id = callback_query.data.replace("category:", "")
    map_id, category_id = map(int, map_category_id.split(":"))

    try:
        text, keyboard = await create_cards_inline(map_id=map_id, category_id=category_id)

        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard
        )
        text_answer = "Выберите карточку"

    except:
        text_answer = "Ошибка выбора категории"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк выбора карточки
@router.callback_query(F.data.startswith("card:"))
async def choice_card_callback_run(callback_query: CallbackQuery):
    map_category_card_id = callback_query.data.replace("card:", "")
    map_id, category_id, card_id = map(int, map_category_card_id.split(":"))

    try:
        card = await sql_get_card_by_id(card_id=card_id)
        image, keyboard = await create_card_images_inline(
            map_id=map_id,
            category_id=category_id,
            card_id=card_id,
            order=1,
            images=card.images
        )

        text = f"""
        <b>{card.name}</b>\n\n
        Описание: {card.description}
        """

        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard,
            media=f"{cfg.IMAGES_DIR}/cards/{image}"
        )
        text_answer = f"Карточка {card.name}"

    except:
        text_answer = "Ошибка выбора карточки"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк навигации по карточке
@router.callback_query(F.data.startswith("image:"))
async def navigation_card_callback_run(callback_query: CallbackQuery):
    map_category_card_order_id = callback_query.data.replace("image:", "")
    map_id, category_id, card_id, order = map(int, map_category_card_order_id.split(":"))

    try:
        image, keyboard = await create_card_images_inline(
            map_id=map_id,
            category_id=category_id,
            card_id=card_id,
            order=order
        )

        await edit_message(
            message=callback_query.message,
            keyboard=keyboard,
            media=f"{cfg.IMAGES_DIR}/cards/{image}"
        )
        text_answer = "Навигация по карточке"

    except:
        text_answer = "Ошибка навигации по карточке"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )