from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text) #сия часть отвечает за тип отправленного сообщения. я хз, но по идее пригодится
async def message_with_text(message: Message):
    msg_sent_time = message.date.strftime("%Y-%m-%d %H:%M:%S")
    await message.answer(
        f"Text message\n"
        f"Отправлено в {msg_sent_time}"
    )

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Sticker")

@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("GIF")

  #  — Здесб хорошо спиться.
  #  — Тся.
  # — Ться.
