# Внешние зависимости
from sqladmin import ModelView
# Внутренние модули
from models import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.telegram_id,
        User.telegram_username,
        User.telegram_first_name,
        User.telegram_last_name,
        User.block_post
    ]

    column_labels = {
        User.id: "Идентификатор",
        User.telegram_id: "Telegram ID",
        User.telegram_username: "Telegram username",
        User.telegram_first_name: "Telegram first name",
        User.telegram_last_name: "Telegram last name",
        User.block_post: "Блокировка на пост карточек",
        "count_create_cards": "Кол-во созданных карточек",
        "count_favorites_cards": "Кол-во карточек в избранном"
    }

    column_searchable_list = [User.telegram_id, User.telegram_id] # список столбцов, которые можно искать
    column_sortable_list = [User.id]  # список столбцов, которые можно сортировать
    column_default_sort = [(User.id, True)]

    column_formatters_detail = {
        "count_create_cards": lambda m, a: len(m.cards) if hasattr(m, 'cards')
                                                                and m.cards else 0,
        "count_favorites_cards": lambda m, a: len(m.favorites) if hasattr(m, 'favorites')
                                                                and m.favorites else 0
    }

    form_edit_rules = [
        "telegram_first_name",
        "telegram_last_name",
        "block_post"
    ]

    column_details_list = [
        User.id,
        User.telegram_id,
        User.telegram_username,
        User.telegram_first_name,
        User.telegram_last_name,
        User.block_post,
        "count_create_cards",
        "count_favorites_cards"
    ]

    can_create = False # право создавать
    can_edit = True # право редактировать
    can_delete = True # право удалять
    can_view_details = True # право смотреть всю информацию
    can_export = True # право экспортировать

    name = "Пользователь" # название
    name_plural = "Пользователи" # множественное название
    icon = "fa-solid fa-circle-user" # иконка
    category = "Пользователи" # категория
    category_icon = "fa-solid fa-list" # иконка категории

    page_size = 10
    page_size_options = [10, 25, 50, 100]