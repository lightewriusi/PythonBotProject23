import asyncio
import logging
from aiogram import Bot, Dispatcher

logging.basicConfig(level=logging.INFO) #Включаем логирование, чтобы видеть, что происходит

async def main():
    bot = Bot(token="7635489387:AAHPul30ZMreG0uCizXaP55nWAn5dMlyrYM") #я не думаю, что он кому-то интересен кроме нас в принципе, но не шалить пж
    dp = Dispatcher() #отслеживаем входящие

    from qschns import router as qschns_router
    from msg_type import router as msg_type_router

    dp.include_routers(qschns_router, msg_type_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) #Запуск процесса поллинга новых апдейтов

if __name__ == "__main__":
    asyncio.run(main())


#Как называется лишение черепахи панциря? # анекдот
# 🐢🐢🐢
#Диспанциризация.
