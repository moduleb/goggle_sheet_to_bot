import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import config
from app.handler import register_handlers


async def main():

    # Создаем бота
    bot = Bot(token=config.TOKEN)
    dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())

    # Регистрируем хендлер
    register_handlers(dispatcher)

    # Запуск
    try:
        print("Bot started...")
        await dispatcher.start_polling(bot)

    finally:
        s = await bot.get_session()
        await s.close()


if __name__ == '__main__':
    asyncio.run(main())
