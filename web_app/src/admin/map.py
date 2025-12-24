# Внешние зависимости
from sqladmin import ModelView
# Внутренние модули
from models import Map


class MapAdmin(ModelView, model=Map):
    column_list = [
        Map.id,
        Map.name,
        Map.image
    ]

    column_labels = {
        Map.id: "Идентификатор",
        Map.name: "Название",
        Map.image: "Изображение",
        Map.categories: "Категории"
    }

    column_searchable_list = [Map.id, Map.name] # список столбцов, которые можно искать
    column_sortable_list = [Map.id]  # список столбцов, которые можно сортировать
    column_default_sort = [(Map.id, True)]

    form_create_rules = [
        "name",
        "image"
    ]

    form_edit_rules = [
        "name",
        "image"
    ]

    column_details_list = [
        Map.id,
        Map.name,
        Map.image,
        Map.categories
    ]

    can_create = True # право создавать
    can_edit = True # право редактировать
    can_delete = True # право удалять
    can_view_details = True # право смотреть всю информацию
    can_export = True # право экспортировать

    name = "Карта" # название
    name_plural = "Карты" # множественное название
    icon = "fa-regular fa-map" # иконка
    category = "Объекты" # категория
    category_icon = "fa-solid fa-list" # иконка категории

    page_size = 10
    page_size_options = [10, 25, 50, 100]