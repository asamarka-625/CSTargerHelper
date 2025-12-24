# Внешние зависимости
from sqladmin import ModelView
from wtforms.validators import ValidationError
# Внутренние модули
from models import Card
from web_app.src.crud import sql_get_mapid_category


class CardAdmin(ModelView, model=Card):
    column_list = [
        Card.id,
        Card.card_number,
        Card.name,
        Card.custom,
        Card.views,
        Card.category,
        Card.user,
        Card.map_id
    ]

    column_labels = {
        Card.id: "Идентификатор",
        Card.name: "Название",
        Card.description: "Описание",
        Card.card_number: "Номер",
        Card.custom: "Пользовательская карточка",
        Card.views: "Просмотры",
        Card.category: "Категория",
        Card.user: "Пользователь",
        Card.images: "Изображения",
        Card.map_id: "ID карты"
    }

    column_searchable_list = [Card.id, Card.card_number, Card.map_id] # список столбцов, которые можно искать
    column_sortable_list = [Card.id, Card.map_id]  # список столбцов, которые можно сортировать
    column_default_sort = [(Card.id, True)]

    async def on_model_change(self, data, model, is_created, request):
        if 'category' in data and data["category"].isdigit():
            try:
                data["map_id"] = await sql_get_mapid_category(category_id=int(data["category"]))

            except:
                ValidationError(f"Ошибка поиска категории: '{data['category']}'")

        return await super().on_model_change(data, model, is_created, request)

    form_create_rules = [
        "name",
        "description",
        "custom",
        "category",
        "user",
        "images"
    ]

    form_edit_rules = [
        "name",
        "description",
        "custom",
        "category",
        "user",
        "images"
    ]

    column_details_list = [
        Card.id,
        Card.name,
        Card.description,
        Card.card_number,
        Card.custom,
        Card.views,
        Card.category,
        Card.user,
        Card.images,
        Card.map_id
    ]

    can_create = True # право создавать
    can_edit = True # право редактировать
    can_delete = True # право удалять
    can_view_details = True # право смотреть всю информацию
    can_export = True # право экспортировать

    name = "Карточка" # название
    name_plural = "Карточки" # множественное название
    icon = "fa-regular fa-address-card" # иконка
    category = "Объекты" # категория
    category_icon = "fa-solid fa-list" # иконка категории

    page_size = 10
    page_size_options = [10, 25, 50, 100]