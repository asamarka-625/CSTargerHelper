# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery
# Внутренние модули
from aiogram.filters import StateFilter
from telegram_bot.keyboards import (create_main_inline, create_maps_inline, create_categories_inline,
                                        create_cards_inline)
from telegram_bot.utils import edit_message
from telegram_bot.core import cfg
from telegram_bot.crud import sql_get_map_image


router = Router()


# Колбэк кнопки назад
@router.callback_query(StateFilter('*'), F.data.startswith("back "))
async def back_callback_run(callback_query: CallbackQuery):
    back = callback_query.data.replace("back ", "")
    data = {}
    cfg.logger.info(f"{back}")
    if back == "main":
        data["text"] = cfg.MAIN_USER_TEXT
        data["keyboard"] = create_main_inline(user_id=callback_query.from_user.id)
        data["media"] = f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"

    elif back == "map":
        data["text"], data["keyboard"] = await create_maps_inline()
        data["media"] = f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"

    elif back.startswith("category:"):
        map_id = int(back.replace("category:", ""))
        data["text"], data["keyboard"] = await create_categories_inline(map_id=map_id)

    elif back.startswith("cards:"):
        map_category_id = back.replace("cards:", "")
        map_id, category_id = map(int, map_category_id.split(":"))

        data["text"], data["keyboard"] = await create_cards_inline(map_id=map_id, category_id=category_id)

        map_image = await sql_get_map_image(map_id=map_id)
        data["media"] = f"{cfg.IMAGES_DIR}/maps/{map_image}"

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