#Файл для проверки сообщений

from aiogram import Bot, Router, F
from aiogram.types import Message

import aiosqlite


router = Router()

@router.message(F.text, F.chat.type.in_({'group', 'supergroup'}))
async def message_with_text(message: Message, bot: Bot):

    #здесь должна быть обработка сообщения, его можно получить через message.text

    #посылание админу (из бд) этой группы текста разразраз; в контактном режиме нам вроде хватит просто сообщения админу
    #собственно тут извлечение админа из бд
    async with aiosqlite.connect('botdb.db') as db:
        async with db.execute("SELECT admin FROM admins WHERE grouptoadmin = '" + str(message.chat.id) + "'") as cursor:
            adminid = (await cursor.fetchone())[0]
    await bot.send_message(adminid, 'разразраз')