# Внешние зависимости
from aiogram import Router
# Внутренние модули
from telegram_bot.handlers.user.message_handler import router as message_router
from telegram_bot.handlers.user.view_cards_callback_handler import router as view_cards_callback_router
from telegram_bot.handlers.user.main_callback_handler import router as main_callback_router


user_router = Router()
user_router.include_router(message_router)
user_router.include_router(view_cards_callback_router)
user_router.include_router(main_callback_router)