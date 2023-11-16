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
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None