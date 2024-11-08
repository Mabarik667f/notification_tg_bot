from .kb_func import add_base_buttons, get_day_name
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .shema import WeekDaysFactory
from src.bot.lexicon.lexicon import LEXICON_BUTTONS, LEXICON
import calendar

obj_calendar = calendar.Calendar(firstweekday=0)
# Клавиатура для кнопок создать и удалить напоминание
notification_methods: list[InlineKeyboardButton] = [InlineKeyboardButton(
    text=LEXICON_BUTTONS['add_notification'],
    callback_data='add_notification'
),
    InlineKeyboardButton(
        text=LEXICON_BUTTONS['list_notifications'],
        callback_data='list_notifications'
    )
]

notification_methods_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
notification_methods_builder.row(*notification_methods, width=2)
notification_methods_kb = notification_methods_builder.as_markup()

# клавиатура часов

confirm = InlineKeyboardButton(text=LEXICON_BUTTONS['confirm'],
                               callback_data='confirm')

select_days: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_BUTTONS['week_days'],
                                                                callback_data='week_days'),
                                           InlineKeyboardButton(text=LEXICON_BUTTONS['exact_date'],
                                                                callback_data='exact_date')]

select_days_builder = InlineKeyboardBuilder()

select_days_builder.row(*select_days, width=2)
add_base_buttons(select_days_builder)
select_days_kb = select_days_builder.as_markup()

day_week_choice: list[InlineKeyboardButton] = []
for day in obj_calendar.iterweekdays():
    day_ru, day_en = get_day_name(day)
    day_button = InlineKeyboardButton(text=day_ru,
                                      callback_data=WeekDaysFactory(**{day_en: True}).pack())
    day_week_choice.append(day_button)

day_week_choice_builder = InlineKeyboardBuilder()
day_week_choice_builder.row(*day_week_choice, width=4)
add_base_buttons(day_week_choice_builder, confirm=confirm)
day_week_choice_kb = day_week_choice_builder.as_markup()


menu = InlineKeyboardButton(text=LEXICON['menu'],
                            callback_data='menu')

menu_kb = InlineKeyboardMarkup(inline_keyboard=[[menu]])

base_builder = InlineKeyboardBuilder()
add_base_buttons(base_builder, confirm=confirm)
base_kb = base_builder.as_markup()

list_notifications_type: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_BUTTONS['date'],
                                                                            callback_data='date'),
                                                       InlineKeyboardButton(text=LEXICON_BUTTONS['week'],
                                                                            callback_data='week'),
                                                       ]

list_notifications_type_builder = InlineKeyboardBuilder()
list_notifications_type_builder.row(*list_notifications_type)
add_base_buttons(list_notifications_type_builder)
list_notifications_type_kb = list_notifications_type_builder.as_markup()


