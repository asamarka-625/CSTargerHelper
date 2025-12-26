# Внешние зависимости
import urllib.parse
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link
# Внутренние модули
from telegram_bot.keyboards import (create_profile_inline, create_back_inline, create_main_menu_inline,
                                        create_main_inline, create_card_images_inline)
from telegram_bot.utils import edit_message, create_short_hash
from telegram_bot.crud import (sql_get_user_info, sql_update_and_get_stats_user, sql_get_card_by_number,
                                   sql_chek_favorite_card_for_user)
from telegram_bot.core import cfg


# Состояние для поиска карточки
class SearchMap(StatesGroup):
    search = State()


router = Router()


# Колбэк перехода в главное меню
@router.callback_query(F.data == "main")
async def redirect_main_callback_run(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback_query.message.answer_photo(
        photo=FSInputFile(f"{cfg.IMAGES_DIR}/main/{cfg.MAIN_USER_PHOTO}"),
        caption=cfg.MAIN_USER_TEXT,
        reply_markup=create_main_inline(user_id=callback_query.from_user.id)
    )

    await callback_query.answer(
        text="Главное меню",
        show_alert=False
    )


# Колбэк получения профиля
@router.callback_query(F.data == "profile")
async def get_profile_callback_run(callback_query: CallbackQuery):
    try:
        user_data = await sql_get_user_info(telegram_id=callback_query.from_user.id)
        user_hash = create_short_hash(*user_data)
        
        keyboard = create_profile_inline(hash_user_data=user_hash)
        
        text = (
            f"username: {user_data[0]}\n"
            f"name: {user_data[1]}\n"
            f"last_name: {user_data[2]}\n"
            f"Кол-во созданных карточек: {user_data[3]}\n"
            f"Кол-во карточек в избранном: {user_data[4]}\n"
        )
        
        await edit_message(
            message=callback_query.message,
            text=text,
            keyboard=keyboard
        )
        text_answer = "Профиль"

    except:
        text_answer = "Ошибка загрузки профиля"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )
    

# Колбэк обновления профиля
@router.callback_query(F.data.startswith("upd_profile:"))
async def update_profile_callback_run(callback_query: CallbackQuery):
    old_user_hash = callback_query.data.replace("upd_profile:", "")
    
    try:
        user_data = await sql_update_and_get_stats_user(
            telegram_id=callback_query.from_user.id,
            telegram_username=callback_query.from_user.username,
            telegram_first_name=callback_query.from_user.first_name,
            telegram_last_name=callback_query.from_user.last_name
        )
        new_user_hash = create_short_hash(*user_data)
        
        if old_user_hash != new_user_hash:
            keyboard = create_profile_inline(hash_user_data=new_user_hash)
            
            text = f"""
            username: @{user_data[0]}\n
            name: {user_data[1]}\n
            last_name: {user_data[2]}\n
            Кол-во созданных карточек: {user_data[3]}\n
            Кол-во карточек в избранном: {user_data[4]}
            """
            
            await edit_message(
                message=callback_query.message,
                text=text,
                keyboard=keyboard
            )
            
        text_answer = "Профиль был обновлен"

    except:
        text_answer = "Ошибка обновления профиля"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Колбэк поиска карточки
@router.callback_query(F.data == "search")
async def search_card_callback_run(callback_query: CallbackQuery, state: FSMContext):
    try:
        keyboard = await create_back_inline("main")

        await edit_message(
            message=callback_query.message,
            text="Напишите номер карточки, которую нужно найти",
            keyboard=keyboard
        )

        text_answer = "Напишите номер карточки"
        await state.set_state(SearchMap.search)

    except:
        text_answer = "Ошибка поиска карточки"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )


# Поиск карточки
@router.message(SearchMap.search)
async def search_card(message: Message, state: FSMContext, bot: Bot):
    card_number = message.text.replace("#", "").upper().strip()
    card = await sql_get_card_by_number(card_number=card_number)

    try:
        if card:
            user_favorite = await sql_chek_favorite_card_for_user(
                telegram_id=message.from_user.id,
                card_id=card.id
            )

            deeplink = await create_start_link(
                bot=bot,
                payload=card.card_number,
                encode=False
            )

            share_link = f"tg://msg_url?url={urllib.parse.quote(deeplink)}"

            image, keyboard = await create_card_images_inline(
                map_id=card.map_id,
                category_id=card.category_id,
                card_id=card.id,
                order=len(card.images),
                user_favorite=int(user_favorite),
                images=card.images,
                share_link=share_link
            )

            text = (
                f"- Изображение {len(card.images)}/{len(card.images)}\n\n"
                f"Номер карточки: <b>#{card.card_number}</b>\n"
                f"Название: <b>{card.name}</b>\n\n"
                f"Описание: {card.description}\n\n"
                f"Ссылка на карточку: <a href='{deeplink}'>Ссылка</a>"
            )

            await message.answer_photo(
                photo=FSInputFile(f"{cfg.IMAGES_DIR}/cards/{image}"),
                caption=text,
                reply_markup=keyboard,
            )

            await state.clear()
            return

    except:
        pass

    await message.answer(
        text="Ничего не найдено, проверьте верность введенного кода и попробуйте еще раз",
        reply_markup=await create_main_menu_inline()
    )