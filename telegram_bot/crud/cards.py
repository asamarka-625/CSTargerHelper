# Внешние зависимости
from typing import Sequence, Tuple
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
# Внутренние модули
from telegram_bot.core import cfg
from models import Card, CardImage
from telegram_bot.core import connection


# Выводим все карточки для категории
@connection
async def sql_get_cards_by_category(category_id: int, session: AsyncSession) -> Sequence[Card]:
    try:
        cards_result = await session.execute(
            sa.select(Card)
            .where(Card.category_id == category_id)
        )
        cards = cards_result.scalars().all()

        return cards

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading all cards by category_id = {category_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading all cards by category_id = {category_id}: {e}")
        raise


# Выводим карточку
@connection
async def sql_get_card_by_id(card_id: int, session: AsyncSession) -> Card:
    try:
        card_result = await session.execute(
            sa.select(Card)
            .where(Card.id == card_id)
            .options(
                so.selectinload(Card.images)
            )
        )
        card = card_result.scalar()

        return card

    except NoResultFound:
        cfg.logger.info(f"Card not found by сard_id = {card_id}")
        raise

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading card by сard_id = {card_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading card by сard_id = {card_id}: {e}")
        raise


# Добавляем новую карточку
@connection
async def sql_add_card(
    name: str,
    description: str,
    category_id: int,
    session: AsyncSession
) -> int:
    try:
        new_card = Card(
            name=name,
            description=description,
            category_id=category_id
        )
        session.add(new_card)
        await session.commit()
        await session.refresh(new_card)

        return new_card.id

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error add new card for category_id = {category_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error add new card for category_id = {category_id}: {e}")
        raise


# Добавляем новое изображение карточки
@connection
async def sql_add_card_image(
    file_name: str,
    order: int,
    card_id: int,
    session: AsyncSession
) -> None:
    try:
        new_card_image = CardImage(
           file_name=file_name,
            order=order,
            card_id=card_id
        )
        session.add(new_card_image)
        await session.commit()

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error add new image for card_id = {card_id}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error add new image for card_id = {card_id}: {e}")
        raise


# Выводим изображение карточки
@connection
async def sql_get_card_image_by_id(
    card_id: int,
    session: AsyncSession,
    order: int
) -> Tuple[bool, bool, str]:
    try:
        images_result = await session.execute(
            sa.select(CardImage.file_name, CardImage.order)
            .where(CardImage.card_id == card_id)
            .options(
                so.selectinload(Card.images)
            )
            .order_by(CardImage.order)
        )
        images = images_result.scalars().all()
        image_i = next((i for i, image in enumerate(images) if image[1] == order), None)

        if image_i is None:
            cfg.logger.info(f"Card not found image by сard_id = {card_id}, order = {order}")
            raise NoResultFound

        return (image_i > 1, image_i < len(images), images[image_i])


    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading image by сard_id = {card_id}, order = {order}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading image by сard_id = {card_id}, order = {order}: {e}")
        raise