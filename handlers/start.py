#handlers/start.py

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from forms_config import FORMS
from keyboards.inline import forms_menu
from core import sheets

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id

    if not sheets.is_user_allowed(user_id):
        await message.answer("❌ У вас нет прав для использования этого бота.")
        return

    await message.answer(
        "Выберите форму:",
        reply_markup=forms_menu(FORMS)
    )

