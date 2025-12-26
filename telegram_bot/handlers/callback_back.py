# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery
# Внутренние модули
from aiogram.filters import StateFilter
from telegram_bot.keyboards import (create_main_inline, create_maps_inline, create_categories_inline,
                                    create_cards_inline, create_my_cards_inline)
from telegram_bot.utils import edit_message
from telegram_bot.core import cfg
from telegram_bot.crud import sql_get_map_image


router = Router()


# Колбэк кнопки назад
@router.callback_query(StateFilter('*'), F.data.startswith("back "))
async def back_callback_run(callback_query: CallbackQuery):
    back = callback_query.data.replace("back ", "")
    data = {}

    if back == "main":
        data["text"] = cfg.MAIN_USER_TEXT
        data["keyboard"] = create_main_inline(user_id=callback_query.from_user.id)
        data["media"] = f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"

    elif back == "map":
        type_card = back.replace("map:", "")
        data["text"], data["keyboard"] = await create_maps_inline(type_card=type_card)
        data["media"] = f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"

    elif back.startswith("category:"):
        type_card, map_id = back.replace("category:", "").split(":")
        map_id = int(map_id)
        data["text"], data["keyboard"] = await create_categories_inline(
            type_card=type_card,
            map_id=map_id
        )

    elif back.startswith("cards:"):
        type_map_category_id = back.replace("cards:", "").split(":")
        type_card = type_map_category_id[0]
        map_id, category_id = map(int, type_map_category_id[1:])

        data["text"], data["keyboard"] = await create_cards_inline(
            telegram_id=callback_query.from_user.id,
            map_id=map_id,
            category_id=category_id,
            type_card=type_card
        )

        map_image = await sql_get_map_image(map_id=map_id)
        data["media"] = f"{cfg.IMAGES_DIR}/maps/{map_image}"

    elif back == "my_cards":
        data["keyboard"] = create_my_cards_inline()
        data["text"] = "Меню ваших карточек"

    else:
        await callback_query.answer(
            text="Ошибка",
            show_alert=False
        )
        return

    await edit_message(
        callback_query.message,
        **data
    )
    await callback_query.answer(text="Назад", show_alert=False)