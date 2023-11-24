from aiogram import Bot

from bot import pool_settings, logger
from src.config import load_config

cfg = load_config()


async def startup(ctx):
    ctx['bot'] = Bot(token=cfg.tg_bot.token)


async def shutdown(ctx):
    await ctx['bot'].session.close()


async def send_message(ctx, chat_id: int, text: str):
    bot: Bot = ctx['bot']
    await bot.send_message(chat_id, text)


class WorkerSettings:
    redis_settings = pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_message, ]