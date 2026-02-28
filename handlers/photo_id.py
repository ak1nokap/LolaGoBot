#handlers/photo_id.py
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.photo)
async def get_photo_id(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.reply(
        f"✅ Ваш file_id:\n<code>{file_id}</code>",
        parse_mode="HTML"
    )