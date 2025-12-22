# Внешние зависимости
from typing import Sequence
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
# Внутренние модули
from telegram_bot.core import cfg
from models import Map
from telegram_bot.core import connection


# Выводим все карты
@connection
async def sql_get_all_maps(session: AsyncSession) -> Sequence[Map]:
    try:
        maps_result = await session.execute(sa.select(Map))
        maps = maps_result.scalars().all()

        return maps

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading all maps: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading all maps: {e}")
        raise


# Добавляем новую карту
@connection
async def sql_add_map(name: str, image: str, session: AsyncSession) -> None:
    try:
        new_map = Map(name=name.lower(), image=image)
        session.add(new_map)
        await session.commit()

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error add new map: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error add new map: {e}")
        raise


# Выводим изображение карты
@connection
async def sql_get_map_image(map_id: int, session: AsyncSession) -> str:
    try:
        image_result = await session.execute(
            sa.select(Map.image)
            .where(Map.id == map_id)
        )
        image = image_result.scalar_one()

        return image

    except NoResultFound:
        cfg.logger.info(f"Card not found map image by map_id = {map_id}")
        raise

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading map image by map_id = {map_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading map image by map_id = {map_id}: {e}")
        raise