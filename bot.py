import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config_data.config import load_config, Config
from keyboards.set_menu import set_main_menu
from handlers import user_handlers, other_handlers

logger = logging.getLogger(__name__)


class NotificationFSM(StatesGroup):
    menu_state = 'menu_state'
    get_text_state = 'get_text'
    choice_days_state = 'choice_days'
    week_days_state = 'week_days'
    exact_day_state = 'exact_day'
    year_choice_state = 'year_choice_state'
    month_choice_state = 'month_choice_state'
    day_choice_state = 'day_choice_state'
    hour_choice_state = 'hour_state'
    minute_state = 'minute_state'
    confirm_data_state = 'confirm_data'
    list_note_state = 'list_note'
    date_note_state = 'date_note_state'
    week_note_state = 'week_note_state'
    delete_note_state = 'delete_note_state'
    activate_note_state = 'activate_note_state'
    delete_exact_note_state = 'delete_exact_note_state'
    delete_week_note_state = 'delete_week_note_state'


cfg: Config = load_config()

redis = Redis(host=cfg.db.db_host, port=6379)
storage = RedisStorage(redis=redis)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Start bot')

    bot = Bot(token=cfg.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await set_main_menu(bot)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())