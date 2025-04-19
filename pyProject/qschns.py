from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

router = Router() #объект, который управляет обработкой команд

def get_who_am_i_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="хто я")]],  # Кнопка в один ряд
        resize_keyboard=True # Автоподгон размера клавиатуры
    )

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Нажми кнопку ниже:",
        reply_markup=get_who_am_i_kb()
    )
# Обработчик xнопки "хто я"

@router.message(F.text.lower() == "хто я")
async def who_am_i(message: Message):
    user = message.from_user

    #Собираем имя
    if user.last_name:
        full_name = f"{user.first_name} {user.last_name}"
    else:
        full_name = user.first_name

    #Статус «поддержал Пашу/не поддержал»
    status = "мажор" if user.is_premium else "вы бережливы"

    #Проверка на бота
    bot_check = "Ага, попався!" if user.is_bot else "Вы не машина"

    #Текущие дата и время
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #тэхт
    text = (
        f"Ваше имя: {full_name}\n"
        f"ID пользователя: {user.id}\n"
        f"Статус: {status}\n"
        f"{bot_check}\n"
        f"Время запроса: {now}"
    )

    # photos = await bot.get_user_profile_photos(user_id) - вроде как рабочий способ получить аватарку (но как же это будет весело)

    #убираем клавиатуру после нажатия
    await message.answer(text, reply_markup=ReplyKeyboardRemove())

    #На чемпионате мира по вежливости победил питерский алкоголик Анатолий, которому не хватало двадцати рублей...#