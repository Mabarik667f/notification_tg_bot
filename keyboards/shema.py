from typing import Optional

from aiogram.filters.callback_data import CallbackData


class CalendarFactory(CallbackData, prefix='ymd', sep='.'):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
