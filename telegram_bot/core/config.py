# Внешние зависимости
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
import logging
# Внутренние модули
from telegram_bot.core.logger import setup_logger


load_dotenv()


@dataclass
class Config:
    _database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL"))
    logger: logging.Logger = field(init=False)

    TELEGRAM_BOT_TOKEN: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN"))

    MAIN_USER_TEXT: str = field(init=False)
    MAIN_ADMIN_TEXT: str = field(init=False)
    IMAGES_DIR: str = field(default_factory=lambda: os.getenv("IMAGES_DIR"))
    MAIN_USER_PHOTO: str = field(default_factory=lambda: os.getenv("MAIN_USER_PHOTO"))
    MAIN_ADMIN_PHOTO: str = field(default_factory=lambda: os.getenv("MAIN_ADMIN_PHOTO"))
    ADMIN_IDS: tuple = field(
        default_factory=lambda: tuple(int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS").split(","))
    )

    LIMIT_VIEW_PAGE: int = field(init=False)

    def __post_init__(self):
        self.logger = setup_logger(
            level=os.getenv("LOG_LEVEL", "INFO"),
            log_dir=os.getenv("LOG_DIR", "logs"),
            log_file=os.getenv("LOG_FILE", "web_log")
        )

        self.MAIN_USER_TEXT: str = "Добро пожаловать!"
        self.MAIN_ADMIN_TEXT: str = "Добро пожаловать, Админ!"

        self.LIMIT_VIEW_PAGE: int = 8

        self.validate()
        self.logger.info("Configuration initialized")

    # Валидация конфигурации
    def validate(self):
        if not self._database_url:
            self.logger.critical("DATABASE_URL is required in environment variables")
            raise ValueError("DATABASE_URL is required")

        self.logger.debug("Configuration validation passed")

    @property
    def DATABASE_URL(self) -> str:
        return self._database_url

    def __str__(self) -> str:
        return f"Config(database={self._database_url}, log_level={self.logger.level})"


_instance = None


def get_config() -> Config:
    global _instance
    if _instance is None:
        _instance = Config()

    return _instance