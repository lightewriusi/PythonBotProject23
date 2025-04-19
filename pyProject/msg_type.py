from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text) #сия часть отвечает за тип отправленного сообщения. я хз, но по идее пригодится
async def message_with_text(message: Message):
    await message.answer("Text message")

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Sticker")

@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("GIF")

  #  — Здесб хорошо спиться.
  #  — Тся.
   # — Ться.