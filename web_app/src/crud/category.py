# Внешние зависимости
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
# Внутренние модули
from web_app.src.core import cfg
from models import Category
from web_app.src.core import connection


# Выводим id карты для категории
@connection
async def sql_get_mapid_category(category_id: int, session: AsyncSession) -> int:
    try:
        mapid_result = await session.execute(
            sa.select(Category.map_id)
            .where(Category.id == category_id)
        )
        map_id = mapid_result.scalar_one()

        return map_id

    except NoResultFound:
        cfg.logger.info(f"Category not found by category_id = {category_id}")
        raise

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading category_id = {category_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading category_id = {category_id}: {e}")
        raise