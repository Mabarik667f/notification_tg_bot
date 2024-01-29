import asyncio

from aiogram import Bot

from celery import Celery
from src.config import load_config

cfg = load_config()


class Config:
    enable_utc = True
    timezone = 'Europe/Moscow'


bot = Bot(token=cfg.tg_bot.token)

app = Celery('main_scheduler', broker='redis://redis:6379/0')
app.config_from_object(Config)


async def send_message(chat_id, text):
    await bot.send_message(chat_id, text)


@app.task(name='exact_date')
def exact_date(chat_id, text):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message(chat_id, text))


# @app.task(name='week_days_date')
# def week_days_date(chat_id, text):
#     print('HI')
#
#
# app.conf.beat_scheduler = {
#     'test': {
#         'task': 'scheduler.week_days_date',
#         'schedule': 10.0
#     }
# }



