import os.path
import pathlib

import asyncio
import logging
from aiogram import Bot, Dispatcher

import aiosqlite

from administering import router as administering_router
from message_checking import router as message_checking_router


logging.basicConfig(level=logging.INFO) #Включаем логирование, чтобы видеть, что происходит

async def main():
    #Если нет файла БД, создаем его (в репозитории его нет)
    if not os.path.isfile(pathlib.Path(pathlib.Path.cwd(), 'botdb.db')):
        async with aiosqlite.connect('botdb.db') as db:
            #Формат: в первой колонке id пользователя, во второй - id группы (c -100)
            await db.execute('CREATE TABLE admins (admin bigint, grouptoadmin bigint)')
            await db.commit()


    bot = Bot(token="")
    dp = Dispatcher() #отслеживаем входящие

    dp.include_routers(administering_router, message_checking_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) #Запуск процесса поллинга новых апдейтов

if __name__ == "__main__":
    asyncio.run(main())


#Как называется лишение черепахи панциря? # анекдот
# 🐢🐢🐢
#Диспанциризация.
