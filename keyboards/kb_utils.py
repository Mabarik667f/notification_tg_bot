from keyboards.kb_func import add_base_buttons, get_day_name
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.shema import WeekDaysFactory
from lexicon.lexicon import LEXICON_BUTTONS, LEXICON
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
add_base_buttons(base_builder)
base_kb = base_builder.as_markup()

