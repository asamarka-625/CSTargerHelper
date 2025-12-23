# Внешние зависимости
import asyncio
# Внутренние модули
from telegram_bot.core import dp, bot, cfg, setup_database
from telegram_bot.middlewares import LoggingMiddleware, ChatActionMiddleware
from telegram_bot.handlers import router


async def main():
    cfg.logger.info("Инициализируем приложение...")

    cfg.logger.info("Инициализируем базу данных")
    await setup_database()

    cfg.logger.info("Инициализируем middlewares")
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    cfg.logger.info("Инициализируем handlers")
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
