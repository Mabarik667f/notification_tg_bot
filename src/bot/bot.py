import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage, Redis
from arq import create_pool
from arq.connections import RedisSettings, ArqRedis

from src.config import load_config, Config
from keyboards.set_menu import set_main_menu
from handlers import user_handlers, other_handlers


logger = logging.getLogger(__name__)


cfg: Config = load_config()

redis = Redis(host=cfg.db.db_host, port=cfg.redis_cfg.port)
storage = RedisStorage(redis=redis)
pool_settings = RedisSettings(host=cfg.redis_cfg.host,
                              port=cfg.redis_cfg.port,
                              database=cfg.redis_cfg.db)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Start bot')

    redis_pool = await create_pool(pool_settings)
    bot = Bot(token=cfg.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await set_main_menu(bot)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           arq_redis=redis_pool,
                           storage=storage)


if __name__ == '__main__':
    asyncio.run(main())

