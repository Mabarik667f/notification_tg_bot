async def save_data_to_redis(storage, key, value):
    await storage.redis.set(key, value)


async def get_data_from_redis(storage, key):
    text = await storage.redis.get(key)
    return text.decode('utf-8')
