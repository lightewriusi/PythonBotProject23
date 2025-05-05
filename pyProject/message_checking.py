from aiogram import Bot, Router, F
from aiogram.types import Message
import aiosqlite

# Импортируем Hugging Face pipeline
from transformers import pipeline
import re  # <== ДОБАВЛЕНО

# Загружаем модель для классификации
classifier = pipeline("text-classification", model="cointegrated/rubert-tiny-toxicity")

router = Router()

def is_gibberish(text):
    # Проверка: много ли подряд одинаковых букв или случайных букв
    return bool(re.fullmatch(r'[а-яА-Яa-zA-Z]{5,}', text.replace(' ', '')) or
                len(re.findall(r'[a-zа-я]{2,}', text.lower())) < 2)


@router.message(F.text, F.chat.type.in_({'group', 'supergroup'}))
async def message_with_text(message: Message, bot: Bot):
    prediction = classifier(message.text)[0]
    label = prediction['label']
    score = prediction['score']

    # Получаем admin id из базы данных
    async with aiosqlite.connect('botdb.db') as db:
        async with db.execute(
                "SELECT admin FROM admins WHERE grouptoadmin = ?", (str(message.chat.id),)
        ) as cursor:
            adminid_row = await cursor.fetchone()
            adminid = adminid_row[0] if adminid_row else None

    if adminid is None:
        return  # Если админ не найден

    # Получаем username или fallback
    if message.from_user.username:
        user_mention = f"@{message.from_user.username}"
    else:
        user_mention = message.from_user.full_name

    # Список плохих лейблов
    bad_labels = ["TOXIC", "INSULT", "OBSCENE", "THREAT"]

    # Проверка на бессмысленный текст (спам)
    is_spam = is_gibberish(message.text)

    # Отправляем админу всё что нам не нравится
    if (label.upper() in bad_labels and score > 0.5) or is_spam:
        if is_spam:
            label_text = "SPAM"
        else:
            label_text = label.upper()

        admin_message = (
            f"Сообщение от {user_mention}:\n\n"
            f"\"{message.text}\"\n\n"
            f"Модель определила как: {label_text}\n"
            f"Рекомендуется забанить человечка"
        )
        await bot.send_message(adminid, admin_message)
