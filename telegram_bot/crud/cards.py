# Внешние зависимости
from typing import Sequence, List, Tuple
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
# Внутренние модули
from telegram_bot.core import cfg
from models import Card, CardImage, User, UserFavorite
from telegram_bot.core import connection


# Выводим все карточки для категории
@connection
async def sql_get_cards_by_category(
    telegram_id: int,
    category_id: int,
    type_card: str,
    session: AsyncSession,
    offset: int = 0
) -> Tuple[bool, bool, Sequence]:
    try:
        query = sa.select(Card.id, Card.name).where(Card.category_id == category_id)

        if type_card == "f":
            query = (
                query
                .join(UserFavorite, Card.id == UserFavorite.card_id)
                .join(User, UserFavorite.user_id == User.id)
                .where(
                    User.telegram_id == telegram_id,
                )
        )

        elif type_card == "m":
            query = (
                query
                .join(User, Card.user_id == User.id)
                .where(
                    User.telegram_id == telegram_id,
                )
            )

        cards_result = await session.execute(
            query
            .offset(offset)
            .limit(cfg.LIMIT_VIEW_PAGE + 1)
        )
        cards = cards_result.all()

        return offset > 0, len(cards) > cfg.LIMIT_VIEW_PAGE, cards[:cfg.LIMIT_VIEW_PAGE]

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading all cards by category_id = {category_id} and type = {type_card}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading all cards by category_id = {category_id} and type = {type_card}: {e}")
        raise


# Выводим карточку по id
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


# Выводим карточку по card_number
@connection
async def sql_get_card_by_number(card_number: str, session: AsyncSession) -> Card:
    try:
        card_result = await session.execute(
            sa.select(Card)
            .where(Card.card_number == card_number)
            .options(
                so.selectinload(Card.images)
            )
        )
        card = card_result.scalar()

        return card

    except NoResultFound:
        cfg.logger.info(f"Card not found by card_number = {card_number}")
        raise

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading card by card_number = {card_number}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading card by card_number = {card_number}: {e}")
        raise


# Добавляем новую карточку
@connection
async def sql_add_card(
    name: str,
    description: str,
    category_id: int,
    custom: bool,
    map_id: int,
    session: AsyncSession
) -> int:
    try:
        new_card = Card(
            name=name.lower(),
            description=description,
            category_id=category_id,
            custom=custom,
            map_id=map_id
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
    file_names: List[str],
    orders: List[int],
    card_id: int,
    session: AsyncSession
) -> None:
    try:
        for file_name, order in zip(file_names, orders):
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
) -> CardImage:
    try:
        image_result = await session.execute(
            sa.select(CardImage)
            .where(
                CardImage.card_id == card_id,
                CardImage.order == order
            )
        )
        image = image_result.scalar_one()

        return image

    except NoResultFound:
        cfg.logger.info(f"Image not found by сard_id = {card_id}, order = {order}")
        raise

    except SQLAlchemyError as e:
        cfg.logger.error(f"Database error reading image by сard_id = {card_id}, order = {order}: {e}")
        raise

    except Exception as e:
        cfg.logger.error(f"Unexpected error reading image by сard_id = {card_id}, order = {order}: {e}")
        raise