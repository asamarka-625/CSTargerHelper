# Внешние зависимости
from typing import Optional, Tuple
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
# Внутренние модули
from telegram_bot.core import cfg
from models import User, Card, UserFavorite
from telegram_bot.core import connection


# Добавляем нового пользователя или обновляем существующего
@connection
async def sql_add_or_update_user(
    telegram_id: int,
    telegram_username: str,
    telegram_first_name: str,
    telegram_last_name: Optional[str],
    session: AsyncSession
) -> None:
    try:
        stmt = sa.insert(User).values(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            telegram_first_name=telegram_first_name,
            telegram_last_name=telegram_last_name
        ).on_conflict_do_update(
            index_elements=['telegram_id'],
            set_={
                'telegram_username': telegram_username,
                'telegram_first_name': telegram_first_name,
                'telegram_last_name': telegram_last_name
            }
        )
        
        await session.execute(stmt)
        await session.commit()

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error add new user or update by telegram_id = {telegram_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error add new user or update by telegram_id = {telegram_id}: {e}")
        raise
        

# Выводим информацию о пользователе
@connection
async def sql_get_user_info(
    telegram_id: int,
    session: AsyncSession
) -> Tuple[Optional[str], Optional[str], Optional[str], int, int]:
    try:
        stmt = sa.select(
            User.telegram_username,
            User.telegram_first_name,
            User.telegram_last_name,
            sa.func.count(Card.id).label('cards_count'),
            sa.func.count(UserFavorite.card_id).label('favorites_count')
        ).select_from(User) \
         .outerjoin(Card, User.id == Card.user_id) \
         .outerjoin(UserFavorite, User.id == UserFavorite.user_id) \
         .where(User.telegram_id == telegram_id) \
         .group_by(User.id)
        
        user_data_result = await session.execute(stmt)
        user_data = user_data_result.first() or ("none", "none", "none", 0, 0)
        
        return user_data
        
    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error get info user by telegram_id = {telegram_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error get info user by telegram_id = {telegram_id}: {e}")
        raise
        
        
# Обновляем данные пользователя
@connection
async def sql_update_and_get_stats_user(
    telegram_id: int,
    telegram_username: str,
    telegram_first_name: str,
    telegram_last_name: Optional[str],
    session: AsyncSession
) -> Tuple[str, str, Optional[str], int, int]:
    try:
        await session.execute(
            sa.update(User)
            .where(User.telegram_id == telegram_id)
            .values(
                telegram_username=telegram_username,
                telegram_first_name=telegram_first_name,
                telegram_last_name=telegram_last_name
            )
        )
        
        stmt = sa.select(
            sa.func.count(Card.id).label('cards_count'),
            sa.func.count(UserFavorite.card_id).label('favorites_count')
        ).select_from(User) \
         .outerjoin(Card, User.id == Card.user_id) \
         .outerjoin(UserFavorite, User.id == UserFavorite.user_id) \
         .where(User.telegram_id == telegram_id) \
         .group_by(User.id)
        
        user_stats_result = await session.execute(stmt)
        await session.commit()

        cards_count, favorites_count = user_stats_result.first() or (0, 0)
        
        return (telegram_username, telegram_first_name, telegram_last_name,
                cards_count, favorites_count)

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error update and get stats user by telegram_id = {telegram_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error update and get stats user by telegram_id = {telegram_id}: {e}")
        raise
        
   