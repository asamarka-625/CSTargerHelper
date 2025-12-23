# Внешние зависимости
from typing import Sequence
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
# Внутренние модули
from telegram_bot.core import cfg
from models import Category
from telegram_bot.core import connection


# Выводим все категории для карты
@connection
async def sql_get_categories_by_map(map_id: int, session: AsyncSession) -> Sequence[Category]:
    try:
        categories_result = await session.execute(
            sa.select(Category)
            .where(Category.map_id == map_id)
        )
        categories = categories_result.scalars().all()

        return categories

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading all categories by map_id = {map_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading all categories by map_id = {map_id}: {e}")
        raise


# Добавляем новую категорию для карты
@connection
async def sql_add_category_for_map(
    name: str,
    map_id: int,
    session: AsyncSession
) -> int:
    try:
        new_category = Category(name=name.lower(), map_id=map_id)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)

        return new_category.id

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error add new category for map_id = {map_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error add new category for map_id = {map_id}: {e}")
        raise