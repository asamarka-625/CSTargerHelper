# Внешние зависимости
from aiogram import Router
# Внутренние модули
from telegram_bot.handlers.user import user_router
from telegram_bot.handlers.admin import admin_router
from telegram_bot.handlers.callback_back import router as back_router
from telegram_bot.handlers.callback_navigation import router as navigation_router


router = Router()
router.include_router(user_router)
router.include_router(admin_router)
router.include_router(navigation_router)
router.include_router(back_router)
