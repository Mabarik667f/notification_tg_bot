from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class RedisConfig:
    db: int
    host: str
    port: int


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    redis_cfg: RedisConfig


def load_config(path: str = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    config = Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD'),
        ),
        redis_cfg=RedisConfig(
            db=int(env('REDIS_DATABASE', 1)),
            host=env('REDIS_HOST', 'redis.conf'),
            port=env('REDIS_PORT')

    )
    )

    return config
