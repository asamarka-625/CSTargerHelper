# Внешние зависимости
from typing import Any, Callable, Dict, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
# Внутренние модули
from telegram_bot.core import cfg

    
class LoggingMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
    
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
         
        user = event.from_user
        
        if isinstance(event, Message):
            if event.text:
                text = event.text.split(' ')
                if len(text) > 1:
                    text = ' '.join(text[1:])
                else:
                    text = text[0]
            else:
                text = 'отправлен объект'

            cfg.logger.info(f'Received MESSAGE from [{user.id}]: [{text}]')

        # Обработка callback-запросов
        elif isinstance(event, CallbackQuery):
            callback_data = event.data
            cfg.logger.info(f'Received CALLBACK from [{user.id}]: [{callback_data}]')

        # Обработка других типов событий
        else:
            event_type = type(event).__name__
            cfg.logger.info(f'Received {event_type} from [{user.id}]')
        
        return await handler(event, data)
