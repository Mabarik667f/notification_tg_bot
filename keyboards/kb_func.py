import calendar
import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .shema import CalendarFactory

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


def create_time_keyboard(j: int, k: int, time_type: str, forward: bool = False,
                         backward: bool = False, width: int = 4) -> InlineKeyboardMarkup:
    time_ls: list[InlineKeyboardButton] = []
    for i in range(j, k):
        text = i
        if i < 10:
            callback_data = f"0{i}_{time_type}"
        else:
            callback_data = f"{i}_{time_type}"
        time_ls.append(InlineKeyboardButton(text=text, callback_data=callback_data))

    time_ls_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    time_ls_builder.row(*time_ls, width=width)
    backward_button, forward_button = _create_move_button(backward=backward, forward=forward)
    add_base_buttons(time_ls_builder, backward=backward_button, forward=forward_button)
    time_ls_kb = time_ls_builder.as_markup()
    return time_ls_kb


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
    days_month = obj_calendar.itermonthdates(year, month)
    return days_month


def add_week_kb(kb):
    week_days: list[InlineKeyboardButton] = [InlineKeyboardButton(text=day_name_ru[key],
                                                                  callback_data=key)
                                             for key in day_name_ru]
    kb.row(*week_days, width=7)


class DialogCalendar:
    @staticmethod
    async def year_calendar():
        current_year = datetime.datetime.now().year
        year_buttons: list[InlineKeyboardButton] = [
            InlineKeyboardButton(
                text=int(current_year) + year,
                callback_data=CalendarFactory(year=int(current_year) + year, month=0, day=0).pack())
            for year in range(0, 4)]

        kb_builder = InlineKeyboardBuilder()
        kb_builder.row(*year_buttons, width=4)
        add_base_buttons(kb_builder)
        return kb_builder.as_markup()

    @staticmethod
    async def get_month(year):
        month_buttons: list[
            InlineKeyboardButton] = []
        for month in range(1, 13):
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

    @staticmethod
    async def get_day(year, month):
        choice_day: list[InlineKeyboardButton] = []
        days = get_days(year, month)
        for day in days:
            d = day.day
            if day.month == month:
                text = str(d)
                callback_data = CalendarFactory(year=year, month=month, day=d).pack()
            else:
                text = ' '
                callback_data = 'ignore_callback'
            day_button = InlineKeyboardButton(text=text,
                                              callback_data=callback_data)
            choice_day.append(day_button)

        day_builder = InlineKeyboardBuilder()
        date_header_buttons(day_builder, year=year, month=month)
        add_week_kb(day_builder)
        day_builder.row(*choice_day, width=7)
        add_base_buttons(day_builder)
        return day_builder.as_markup()
