# Внешние зависимости
from aiogram import Router
# Внутренние модули
from telegram_bot.handlers.user.message_handler import router as message_router
from telegram_bot.handlers.user.callback_handler import router as callback_router


user_router = Router()

user_router.include_router(message_router)
user_router.include_router(callback_router)