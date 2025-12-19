# Внешние зависимости
from aiogram import Router
# Внутренние модули
from telegram_bot.handlers.admin.admin_handler import router as main_router
from telegram_bot.handlers.admin.admin_add_category import router as add_category_router
from telegram_bot.handlers.admin.admin_add_map import router as add_map_router
from telegram_bot.handlers.admin.admin_add_card import router as add_card_router


admin_router = Router()
admin_router.include_router(main_router)
admin_router.include_router(add_map_router)
admin_router.include_router(add_category_router)
admin_router.include_router(add_card_router)