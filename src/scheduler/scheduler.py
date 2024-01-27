from aiogram import Bot

from celery import Celery

# cfg = load_config()


class Config:
    enable_utc = True
    timezone = 'Europe/Moscow'


app = Celery('main_scheduler', broker='redis.conf://localhost:6379/0')
app.config_from_object(Config)


@app.task
def mes():
    print(f"Hi")


n = 10
res = mes.apply_async(coutdown=10)

