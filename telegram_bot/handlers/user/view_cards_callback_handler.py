# Внешние зависимости
import urllib.parse
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
# Внутренние модули
from telegram_bot.keyboards import (create_maps_inline, create_categories_inline, create_cards_inline,
                                        create_card_images_inline)
from telegram_bot.utils import edit_message
from telegram_bot.crud import (sql_get_card_by_id, sql_get_map_image, sql_chek_favorite_card_for_user,
                               sql_update_favorite_card_for_user)
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
async def choice_card_callback_run(callback_query: CallbackQuery, bot: Bot):
    map_category_card_id = callback_query.data.replace("card:", "")
    map_id, category_id, card_id = map(int, map_category_card_id.split(":"))

    try:
        card = await sql_get_card_by_id(card_id=card_id)
        user_favorite = await sql_chek_favorite_card_for_user(
            telegram_id=callback_query.from_user.id,
            card_id=card_id
        )

        deeplink = await create_start_link(
            bot=bot,
            payload=card.card_number,
            encode=False
        )

        share_link = f"tg://msg_url?url={urllib.parse.quote(deeplink)}"

        text = (
            f"- Изображение {len(card.images)}/{len(card.images)}\n\n"
            f"Номер карточки: <b>#{card.card_number}</b>\n"
            f"Название: <b>{card.name}</b>\n\n"
            f"Описание: {card.description}\n\n"
            f"Ссылка на карточку: <a href='{deeplink}'>Ссылка</a>"
        )

        image, keyboard = await create_card_images_inline(
            map_id=map_id,
            category_id=category_id,
            card_id=card_id,
            order=len(card.images),
            user_favorite=int(user_favorite),
            images=card.images,
            share_link=share_link
        )

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
async def navigation_card_callback_run(callback_query: CallbackQuery, bot: Bot):
    favorite_map_category_card_image_order_id = callback_query.data.replace("image:", "")
    favorite, map_id, category_id, card_id, max_image, order = \
        map(int, favorite_map_category_card_image_order_id.split(":"))

    try:
        if order > max_image:
            order = 1

        caption_split = callback_query.message.caption.split("\n")

        card_number = caption_split[2].replace("Номер карточки: #", "").strip()
        deeplink = await create_start_link(
            bot=bot,
            payload=card_number,
            encode=False
        )

        share_link = f"tg://msg_url?url={urllib.parse.quote(deeplink)}"

        image, keyboard = await create_card_images_inline(
            map_id=map_id,
            category_id=category_id,
            card_id=card_id,
            order=order,
            user_favorite=favorite,
            max_image=max_image,
            share_link=share_link
        )

        caption = "\n".join(caption_split[4:-1])
        text = (
            f"- Изображение {order}/{max_image}\n\n"
            f"Номер карточки: <b>#{card_number}</b>\n"
            f"Название: <b>{caption_split[3].replace("Название: ", "").strip()}</b>\n"
            f"{caption}\n"
            f"Ссылка на карточку: <a href='{deeplink}'>Ссылка</a>"
        )

        await edit_message(
            message=callback_query.message,
            text=text,
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


# Колбэк добавления/удаления из избранного
@router.callback_query(F.data.startswith("favorite:"))
async def favorite_card_callback_run(callback_query: CallbackQuery, bot: Bot):
    favorite_map_category_card_image_order_id = callback_query.data.replace("favorite:", "")
    favorite, map_id, category_id, card_id, max_image, order = \
        map(int, favorite_map_category_card_image_order_id.split(":"))

    try:
        await sql_update_favorite_card_for_user(
            telegram_id=callback_query.from_user.id,
            card_id=card_id,
            favorite=bool(favorite)
        )

        card_number = callback_query.message.caption.split("\n")[0].replace("Номер карточки: #", "").strip()
        deeplink = await create_start_link(
            bot=bot,
            payload=card_number,
            encode=False
        )

        share_link = f"tg://msg_url?url={urllib.parse.quote(deeplink)}"

        _, keyboard = await create_card_images_inline(
            map_id=map_id,
            category_id=category_id,
            card_id=card_id,
            order=order,
            user_favorite=int(not favorite),
            max_image=max_image,
            share_link=share_link
        )

        await edit_message(
            message=callback_query.message,
            keyboard=keyboard
        )

        if favorite:
            text_answer = "Удалено из избранного"

        else:
            text_answer = "Успешно добавлено в избранное"

    except:
        import traceback
        traceback.print_exc()
        text_answer = "Ошибка изменения избранного"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )