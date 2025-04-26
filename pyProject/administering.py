#Файл для взаимодействия с админом

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from aiogram.enums import ParseMode

import aiosqlite


router = Router() #объект, который управляет обработкой команд

#Просто стартовое сообщений
@router.message(Command("start"), F.chat.type.in_({'private'}))
async def cmd_start(message: Message, command: CommandObject):
    await message.answer('Привет! Я - бот для борьбы с нейрокомментированием.\n\n<a href="https://github.com/ShestakovID/PythonBotProject">Репозиторий</a>\n\nДобавить группу - /addgroup &lt;id группы (с -100)&gt;', parse_mode=ParseMode.HTML)

#Добавить себя админом группы
@router.message(Command("addgroup"), F.chat.type.in_({'private'}))
async def cmd_start(message: Message, command: CommandObject):
    if command.args:
        async with aiosqlite.connect('botdb.db') as db:
            async with db.execute('SELECT * FROM admins WHERE grouptoadmin = \'' + command.args + '\'') as cursor:
                adminofthisgroup = await cursor.fetchall()
            if adminofthisgroup == []:
                await db.execute('INSERT INTO admins (admin,grouptoadmin) VALUES (\'' + str(message.from_user.id) + '\', \'' + command.args  + '\')')
                await db.commit()
            else:
                await message.answer('У этой группы уже есть админ')
    else:
        await message.answer('Неправильный формат команды')