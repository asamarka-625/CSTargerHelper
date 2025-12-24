# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery
# Внутренние модули
from aiogram.filters import StateFilter
from telegram_bot.keyboards import create_maps_inline, create_categories_inline, create_cards_inline
from telegram_bot.utils import edit_message
from telegram_bot.core import cfg


router = Router()


# Колбэк кнопок навигации
@router.callback_query(
    StateFilter('*'),
    F.data.startswith("prev ") | F.data.startswith("next ")
)
async def prev_next_callback_run(callback_query: CallbackQuery):
    if callback_query.data.startswith("prev "):
        nav = callback_query.data.replace("prev ", "")
        page_up = -1
    else:
        nav = callback_query.data.replace("next ", "")
        page_up = 1

    data = {}
    if nav.startswith("map"):
        if nav.startswith("map-admin"):
            admin = True
            nav = nav.replace("map-admin:", "")

        else:
            admin = False
            nav = nav.replace("map:", "")

        page = int(nav)

        data["text"], data["keyboard"] = await create_maps_inline(
            offset=(page - page_up) * cfg.LIMIT_VIEW_PAGE,
            admin=admin
        )

    elif nav.startswith("category"):
        if nav.startswith("category-admin"):
            admin = True
            nav = nav.replace("category-admin:", "")

        else:
            admin = False
            nav = nav.replace("category:", "")

        map_id, page = map(int, nav.split(":"))

        data["text"], data["keyboard"] = await create_categories_inline(
            map_id=map_id,
            offset=(page - page_down) * cfg.LIMIT_VIEW_PAGE,
            admin=admin
        )

    elif nav.startswith("card"):
        map_category_page = nav.replace("card:", "")
        map_id, category_id, page = map(int, map_category_page.split(":"))

        data["text"], data["keyboard"] = await create_cards_inline(
            map_id=map_id,
            category_id=category_id,
            offset=(page - page_down) * cfg.LIMIT_VIEW_PAGE
        )

    else:
        await callback_query.answer(
            text="Ошибка навигации",
            show_alert=False
        )
        return

    await edit_message(
        callback_query.message,
        **data
    )

    await callback_query.answer(text="Предыдущая страница", show_alert=False)