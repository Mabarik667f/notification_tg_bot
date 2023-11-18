import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .shema import CalendarFactory, WeekDaysFactory

from lexicon.lexicon import LEXICON_BUTTONS, LEXICON, day_name_ru, month_name_ru


def add_base_buttons(keyboard: InlineKeyboardBuilder, backward: InlineKeyboardButton = False,
                     forward: InlineKeyboardButton = False,
                     confirm: InlineKeyboardButton = False) -> None:
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_BUTTONS['menu'],
                                                                callback_data='menu'),
                                           InlineKeyboardButton(text=LEXICON['back'],
                                                                callback_data='back')]
    if backward:
        buttons.insert(0, backward)
    if forward:
        buttons.append(forward)

    keyboard.row(*buttons, width=4)
    if confirm:
        keyboard.row(confirm, width=1)


def _create_move_button(forward: bool = False, backward: bool = False) -> tuple:
    backward_button, forward_button = False, False
    if backward:
        backward_button = (InlineKeyboardButton(text=LEXICON_BUTTONS['backward'],
                                                callback_data=LEXICON_BUTTONS['backward']))
    if forward:
        forward_button = (InlineKeyboardButton(text=LEXICON_BUTTONS['forward'],
                                               callback_data=LEXICON_BUTTONS['forward']))

    return backward_button, forward_button


# нужно закинуть сюда выбранный год из redis и месяц
def date_header_buttons(builder: InlineKeyboardBuilder, year, month=False):
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=' ',
                                                                callback_data='ignore_callback'),
                                           InlineKeyboardButton(text=year,
                                                                callback_data='ignore_callback')
                                           ]
    if month:
        ru, en = get_month_name(month)
        button = InlineKeyboardButton(text=ru,
                                      callback_data='ignore_callback')
    else:
        button = InlineKeyboardButton(text=' ',
                                      callback_data='ignore_callback')
    buttons.append(button)
    builder.row(*buttons, width=3)


def get_day_name(day_number):
    day_name_en = calendar.day_name[day_number]

    return day_name_ru[day_name_en], day_name_en


def get_month_name(month_number):
    month_name_en = calendar.month_name[month_number]

    return month_name_ru[month_name_en], month_name_en


obj_calendar = calendar.Calendar(firstweekday=0)


def get_days(year, month):
    days_month = obj_calendar.itermonthdays(year, month)
    return days_month


def add_week_kb(kb):
    week_days: list[InlineKeyboardButton] = [InlineKeyboardButton(text=day_name_ru[key],
                                                                  callback_data=key)
                                             for key in day_name_ru]
    kb.row(*week_days, width=7)


class DialogCalendar:

    def __init__(self):
        self.curr_year = datetime.now().year
        self.curr_month = datetime.now().month
        self.curr_day = datetime.now().day
        self.curr_hour = datetime.now().hour
        self.curr_minute = datetime.now().minute
        self.base_button = InlineKeyboardButton(text=' ',
                                                callback_data='ignore_callback')

    async def year_calendar(self):
        year_buttons: list[InlineKeyboardButton] = [
            InlineKeyboardButton(
                text=int(self.curr_year) + year,
                callback_data=CalendarFactory(year=int(self.curr_year) + year, month=0, day=0).pack())
            for year in range(0, 4)]

        kb_builder = InlineKeyboardBuilder()
        kb_builder.row(*year_buttons, width=4)
        add_base_buttons(kb_builder)
        return kb_builder.as_markup()

    async def get_month(self, year):
        month_buttons: list[
            InlineKeyboardButton] = []

        start_month = 1
        if year == self.curr_year:
            start_month = self.curr_month

        for month in range(start_month, 13):
            month_ru, month_en = get_month_name(month)
            month_button = InlineKeyboardButton(
                text=month_ru,
                callback_data=CalendarFactory(year=year, month=month).pack())
            month_buttons.append(month_button)

        month_builder = InlineKeyboardBuilder()
        date_header_buttons(month_builder, year)
        month_builder.row(*month_buttons, width=3)
        add_base_buttons(month_builder)
        return month_builder.as_markup()

    async def get_day(self, year, month):
        choice_day: list[InlineKeyboardButton] = []
        days = get_days(year, month)

        for day in days:
            if month == self.curr_month and day < self.curr_day and year == self.curr_year:
                day_button = self.base_button
            elif month == self.curr_month and year == self.curr_year and self.curr_minute == 59 and self.curr_hour == 23:
                day_button = self.base_button
            elif day != 0:
                day_button = InlineKeyboardButton(
                    text=day,
                    callback_data=CalendarFactory(year=year, month=month, day=day).pack()
                )
            else:
                day_button = self.base_button

            day_button = day_button
            choice_day.append(day_button)

        day_builder = InlineKeyboardBuilder()
        date_header_buttons(day_builder, year=year, month=month)
        add_week_kb(day_builder)
        for i in range(0, len(choice_day), 7):
            if all(i == self.base_button for i in choice_day[i:i + 7]):
                continue
            else:
                day_builder.row(*choice_day[i:i + 7], width=7)
        add_base_buttons(day_builder)
        return day_builder.as_markup()

    async def get_hour(self, year, month, day):
        choice_hours: list[InlineKeyboardButton] = []
        beg = 0
        if day == self.curr_day and month == self.curr_month and self.curr_year == year:
            beg = self.curr_hour
            while beg % 4 != 0:
                beg -= 1
        for hour in range(beg, 24):
            if day == self.curr_day and month == self.curr_month and self.curr_year == year and self.curr_hour > hour:
                hour_button = self.base_button
            elif day == self.curr_day and month == self.curr_month and self.curr_year == year and \
                    self.curr_minute == 59:
                hour_button = self.base_button
            else:
                hour_button = InlineKeyboardButton(
                    text=hour,
                    callback_data=CalendarFactory(year=year, month=month, day=day, hour=hour).pack())

            choice_hours.append(hour_button)

        hour_builder = InlineKeyboardBuilder()
        for i in range(0, len(choice_hours), 4):
            if all(i == self.base_button for i in choice_hours[i:i + 4]):
                continue
            else:
                hour_builder.row(*choice_hours[i:i + 4], width=4)
        add_base_buttons(hour_builder)
        return hour_builder.as_markup()

    async def get_minutes(self, year, month, day, hour):
        choice_minutes: list[InlineKeyboardButton] = []
        beg = 0
        if day == self.curr_day and month == self.curr_month and self.curr_year == year \
                and self.curr_hour == hour:
            beg = self.curr_minute
            if beg == 59:
                year, month, day, hour, minute = self.check_time(year, month, day, hour, beg)
            while beg % 5 != 0:
                beg -= 1
        for minute in range(beg, 60):
            if day == self.curr_day and month == self.curr_month and self.curr_year == year \
                    and self.curr_hour == hour and (self.curr_minute > minute or self.curr_minute == minute):
                minute_button = self.base_button
            else:
                minute_button = InlineKeyboardButton(
                    text=minute,
                    callback_data=CalendarFactory(year=year, month=month, day=day,
                                                  hour=hour, minute=minute).pack())

            choice_minutes.append(minute_button)

        minute_builder = InlineKeyboardBuilder()
        for i in range(0, len(choice_minutes), 5):
            if all(i == self.base_button for i in choice_minutes[i:i + 5]):
                continue
            else:
                minute_builder.row(*choice_minutes[i:i + 5], width=5)
        add_base_buttons(minute_builder)
        return minute_builder.as_markup()

    def check_time(self, year, month, day, hour, minute):
        if hour == 23 and (hour == self.curr_hour and day == self.curr_day and month == self.curr_month and
                           minute == self.curr_minute):
            hour, minute = 0, 0
            _, last_day_of_month = calendar.monthrange(year, month)
            if day == last_day_of_month:
                day = 1
                if month + 1 > 12:
                    month = 1
                    return year + 1, month, day, hour, minute
                else:
                    return year, month + 1, day, hour, minute
            else:
                return year, month, day + 1, hour, minute
        elif hour != 23 and hour == self.curr_hour and minute == self.curr_minute:
            minute = 0
            return year, month, day, hour + 1, minute
        return year, month, day, hour, minute


class WeekDayDate:

    def __init__(self):
        self.days = []
        self.data = {}

    async def get_hour(self):
        choice_hours: list[InlineKeyboardButton] = []
        for hour in range(0, 24):
            hour_button = InlineKeyboardButton(
                text=hour,
                callback_data=WeekDaysFactory(hour=hour, minute=None, **self.data).pack())

            choice_hours.append(hour_button)

        hour_builder = InlineKeyboardBuilder()
        hour_builder.row(*choice_hours, width=4)
        add_base_buttons(hour_builder)
        return hour_builder.as_markup()

    async def get_minute(self, hour):
        choice_minutes: list[InlineKeyboardButton] = []
        for minute in range(0, 60):
            minute_button = InlineKeyboardButton(
                text=minute,
                callback_data=WeekDaysFactory(hour=hour, minute=minute, **self.data).pack())

            choice_minutes.append(minute_button)

        minute_builder = InlineKeyboardBuilder()
        minute_builder.row(*choice_minutes, width=5)
        add_base_buttons(minute_builder)
        return minute_builder.as_markup()
