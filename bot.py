import asyncio
import logging

from aiogram import Dispatcher, Bot
from config_data.config import load_config, Config
from keyboards.set_menu import set_main_menu
from handlers import user_handlers, other_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Start bot')

    cfg: Config = load_config()

    bot = Bot(token=cfg.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    await set_main_menu(bot)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())