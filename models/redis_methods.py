from bot import storage


async def save_data_to_redis(key, value):
    await storage.redis.set(key, value)


async def get_data_from_redis(key):
    text = await storage.redis.get(key)
    return text.decode('utf-8')
