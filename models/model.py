# Внешние зависимости
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
# Внутренние модули
from models.base import Base


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
    card_number: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        unique=True,
        index=True,
        nullable=False
    )
    custom: so.Mapped[bool] = so.mapped_column(
        sa.Boolean,
        nullable=False
    )
    views: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        nullable=False,
        default=0
    )
    
    # Внешние ключи
    category_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    user_id: so.Mapped[Optional[int]] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
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
    user: so.Mapped["User"] = so.relationship(
        "User",
        back_populates="cards"
    )

    def __repr__(self):
        return f"<Card(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name
        

# Модель для связи cards и users (избранное)
class UserFavorite(Base):
    __tablename__ = "user_favorites"
    
    user_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    card_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey('cards.id', ondelete='CASCADE'),
        primary_key=True
    )
    
    __table_args__ = (
        sa.UniqueConstraint('user_id', 'card_id', name='uq_user_favorite'),
    )

    
# Модель Пользователя
class User(Base):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    telegram_id: so.Mapped[int] = so.mapped_column(
        sa.BigInteger,
        unique=True,
        index=True,
        nullable=False
    )
    telegram_username: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(32),
        nullable=True
    )
    telegram_first_name: so.Mapped[str] = so.mapped_column(
        sa.String(64),
        nullable=False
    )
    telegram_last_name: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(64),
        nullable=True
    )
    block_post: so.Mapped[bool] = so.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False
    )

    # Связи
    cards: so.Mapped[List["Card"]] = so.relationship(
        "Card",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    favorites: so.Mapped[List["Card"]] = so.relationship(
        "Card",
        secondary="user_favorites",
        backref="favorited_by"
    )

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id='{self.telegram_id}', telegram_username='{self.telegram_username}')>"

    def __str__(self):
        return self.telegram_id