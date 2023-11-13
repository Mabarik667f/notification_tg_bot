import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.state import StatesGroup

from config_data.config import load_config, Config
from keyboards.set_menu import set_main_menu
from handlers import user_handlers, other_handlers

logger = logging.getLogger(__name__)


class NotificationFSM(StatesGroup):
    minutes_15_state = 'minutes_15'
    minutes_30_state = 'minutes_30'
    minutes_45_state = 'minutes_45'
    minutes_60_state = 'minutes_60'
    hour_choice_state = 'hour_state'
    menu_state = 'menu_state'
    choice_days_state = 'choice_days'
    exact_day_state = 'exact_day'
    week_days_state = 'week_days'
    year_choice_state = 'year_choice_state'
    month_choice_state = 'month_choice_state'


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
    dp.include_router(other_handlers.router)

    await set_main_menu(bot)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())