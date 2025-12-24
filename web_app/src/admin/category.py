# Внешние зависимости
from sqladmin import ModelView
# Внутренние модули
from models import Category


class CategoryAdmin(ModelView, model=Category):
    column_list = [
        Category.id,
        Category.name,
        Category.map
    ]

    column_labels = {
        Category.id: "Идентификатор",
        Category.name: "Название",
        Category.map: "Карты",
        "count_cards": "Кол-во карточек"
    }

    column_searchable_list = [Category.id] # список столбцов, которые можно искать
    column_sortable_list = [Category.id]  # список столбцов, которые можно сортировать
    column_default_sort = [(Category.id, True)]

    column_formatters_detail = {
        "count_cards": lambda m, a: len(m.cards) if hasattr(m, 'cards') and m.cards else 0
    }

    form_create_rules = [
        "name",
        "map"
    ]

    form_edit_rules = [
        "name",
        "map"
    ]

    column_details_list = [
        Category.id,
        Category.name,
        Category.map,
        "count_cards"
    ]

    can_create = True # право создавать
    can_edit = True # право редактировать
    can_delete = True # право удалять
    can_view_details = True # право смотреть всю информацию
    can_export = True # право экспортировать

    name = "Категория" # название
    name_plural = "Категории" # множественное название
    icon = "fa-solid fa-book" # иконка
    category = "Объекты" # категория
    category_icon = "fa-solid fa-list" # иконка категории

    page_size = 10
    page_size_options = [10, 25, 50, 100]