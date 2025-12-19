from telegram_bot.core.config import get_config
from telegram_bot.core.database import setup_database, connection, engine
from telegram_bot.core.create_bot import dp, bot


cfg = get_config()