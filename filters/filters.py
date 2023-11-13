from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDateTimePostfixCallbackData(BaseFilter):
    def __init__(self, postfix):
        self.postfix = postfix

    async def __call__(self, callback):
        return callback.data.endswith(self.postfix)
