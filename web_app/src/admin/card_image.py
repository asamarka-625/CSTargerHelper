# Внешние зависимости
from sqladmin import ModelView
# Внутренние модули
from models import CardImage


class CardImageAdmin(ModelView, model=CardImage):
    column_list = [
        CardImage.id,
        CardImage.file_name,
        CardImage.order,
        CardImage.card
    ]

    column_labels = {
        CardImage.id: "Идентификатор",
        CardImage.file_name: "Название файла",
        CardImage.order: "Порядковый номер изображения",
        CardImage.card: "Карточка"
    }

    column_searchable_list = [CardImage.id] # список столбцов, которые можно искать
    column_sortable_list = [CardImage.id]  # список столбцов, которые можно сортировать
    column_default_sort = [(CardImage.id, True)]

    form_create_rules = [
        "file_name",
        "order",
        "card"
    ]

    form_edit_rules = [
        "file_name",
        "order",
        "card"
    ]

    column_details_list = [
        CardImage.id,
        CardImage.file_name,
        CardImage.order,
        CardImage.card
    ]

    can_create = True # право создавать
    can_edit = True # право редактировать
    can_delete = True # право удалять
    can_view_details = True # право смотреть всю информацию
    can_export = True # право экспортировать

    name = "Изображение" # название
    name_plural = "Изображения" # множественное название
    icon = "fa-solid fa-images" # иконка
    category = "Объекты" # категория
    category_icon = "fa-solid fa-list" # иконка категории

    page_size = 10
    page_size_options = [10, 25, 50, 100]