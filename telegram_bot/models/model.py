# Внешние зависимости
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
# Внутренние модули
from telegram_bot.models.base import Base


# Модель Карты
class Map(Base):
    __tablename__ = "maps"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(
        sa.String(255),
        unique=True,
        index=True,
        nullable=False
    )
    image: so.Mapped[str] = so.mapped_column(
        sa.String(128),
        nullable=False,
    )

    # Связи
    categories: so.Mapped[List["Category"]] = so.relationship(
        "Category",
        back_populates="map",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Map(id={self.id}, name='{self.name}', image='{self.image}')>"

    def __str__(self):
        return self.name


# Модель Категории
class Category(Base):
    __tablename__ = 'categories'

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(
        sa.String(255),
        nullable=False
    )

    # Внешние ключи
    map_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('maps.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Связи
    map: so.Mapped["Map"] = so.relationship(
        "Map",
        back_populates="categories"
    )
    cards: so.Mapped[List["Card"]] = so.relationship(
        "Card",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, map_id={self.map_id}, name='{self.name}')>"

    def __str__(self):
        return self.name


# Модель Изображения
class CardImage(Base):
    __tablename__ = "card_images"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    file_name: so.Mapped[str] = so.mapped_column(
        sa.String(128),
        nullable=False,
    )
    order: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        default=1,
        nullable=False,
        index=True
    )

    # Внешние ключи
    card_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('cards.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Связи
    card: so.Mapped["Card"] = so.relationship(
        "Card",
        back_populates="images"
    )

    __table_args__ = (
        sa.UniqueConstraint('card_id', 'order', name='uq_card_image_order'),
    )

    def __repr__(self):
        return f"<CardImage(id={self.id}, card_id={self.card_id}, file_name='{self.file_name}')>"

    def __str__(self):
        return self.file_name


# Модель карточки
class Card(Base):
    __tablename__ = "cards"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(
        sa.String(255),
        nullable=False
    )
    description: so.Mapped[str] = so.mapped_column(
        sa.String(1024),
        nullable=False
    )

    # Внешние ключи
    category_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Связи
    category: so.Mapped["Category"] = so.relationship(
        "Category",
        back_populates="cards"
    )
    images: so.Mapped[List["CardImage"]] = so.relationship(
        "CardImage",
        back_populates="card",
        cascade="all, delete-orphan",
        order_by="CardImage.order"
    )

    def __repr__(self):
        return f"<Card(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name