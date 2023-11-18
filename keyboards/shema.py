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
    Monday: Optional[int] = None
    Tuesday: Optional[int] = None
    Wednesday: Optional[bool] = None
    Thursday: Optional[bool] = None
    Friday: Optional[bool] = None
    Saturday: Optional[bool] = None
    Sunday: Optional[bool] = None

    def __iter__(self):
        for key, value in self.__dict__.items():
            if key.endswith('day') and value:
                yield key

