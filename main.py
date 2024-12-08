import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import load_config, Config
from handler import other_handler, user_handler

logger = logging.getLogger(__name__)

async def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # регистрация роутеров
    dp.include_router(user_handler.router)
    dp.include_router(other_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
