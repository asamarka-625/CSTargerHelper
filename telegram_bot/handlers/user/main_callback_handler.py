# Внешние зависимости
from aiogram import Router, F
from aiogram.types import CallbackQuery
# Внутренние модули
from telegram_bot.keyboards import create_profile_inline
from telegram_bot.utils import edit_message, create_short_hash
from telegram_bot.crud import sql_get_user_info, sql_update_and_get_stats_user


router = Router()


# Колбэк получения профиля
@router.callback_query(F.data == "profile")
async def get_profile_callback_run(callback_query: CallbackQuery):
    try:
        user_data = await sql_get_user_info(telegram_id=callback_query.from_user.id)
        user_hash = create_short_hash(*user_data)
        
        keyboard = create_profile_inline(hash_user_data=user_hash)
        
        text = f"""
        username: {user_data[0]}\n
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
        text_answer = "Профиль"

    except:
        text_answer = "Ошибка загрузки профиля"

    await callback_query.answer(
        text=text_answer,
        show_alert=False
    )
    

# Колбэк обновления профиля
@router.callback_query(F.data == "upd_profile:")
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
            username: {user_data[0]}\n
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