#app.py

import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, form, id, photo_id

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(form.router)
    dp.include_router(id.router)
    dp.include_router(photo_id.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())