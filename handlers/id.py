#handlers/id.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=["id"]))
async def send_user_id(message: Message):
    user_id = message.from_user.id
    await message.answer(f"Ваш Telegram user_id: {user_id}")

@router.message(Command(commands=["chatid"]))
async def get_group_id(message: Message):
    await message.answer(f"Chat ID этой группы: {message.chat.id}")