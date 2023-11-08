from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsTimeCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('_add') and callback.data not in ['custom_add', 'day_add']


class IsHourCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('hour')
