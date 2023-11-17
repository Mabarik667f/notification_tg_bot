from typing import Optional

from aiogram.filters.callback_data import CallbackData


class CalendarFactory(CallbackData, prefix='ymd', sep='.'):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None


class WeekDaysFactory(CallbackData, prefix='weekday', sep='|'):
    hour: Optional[int] = None
    minute: Optional[int] = None
    monday: Optional[int] = None
    tuesday: Optional[int] = None
    wednesday: Optional[int] = None
    thursday: Optional[int] = None
    friday: Optional[int] = None
    saturday: Optional[int] = None
    sunday: Optional[int] = None