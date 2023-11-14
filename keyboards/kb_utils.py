import datetime

from keyboards.kb_func import add_base_buttons, create_time_keyboard, get_day_name, get_month_name, date_header_buttons, \
    get_days, add_week_kb
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_BUTTONS
from services.services import get_curr_date
import calendar

obj_calendar = calendar.Calendar(firstweekday=0)
# Клавиатура для кнопок создать и удалить напоминание
notification_methods: list[InlineKeyboardButton] = [InlineKeyboardButton(
    text=LEXICON_BUTTONS['add_notification'],
    callback_data='add_notification'
),
    InlineKeyboardButton(
        text=LEXICON_BUTTONS['remove_notification'],
        callback_data='remove_notification'
    )
]

notification_methods_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
notification_methods_builder.row(*notification_methods, width=2)
notification_methods_kb = notification_methods_builder.as_markup()

# Клавиатура с пулом возможных для создания напоминаний


notification_add: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_BUTTONS[key],
                                                                     callback_data=key)
                                                for key in LEXICON_BUTTONS.keys()
                                                if key.endswith('_add')]

notification_add_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
notification_add_builder.row(*notification_add, width=3)
add_base_buttons(notification_add_builder)
notification_add_kb = notification_add_builder.as_markup()

# клавиатура часов

hour_choice = create_time_keyboard(0, 24, 'hour')

minutes_15 = create_time_keyboard(0, 15, 'minute', forward=True, width=5)
minutes_30 = create_time_keyboard(15, 30, 'minute', forward=True, backward=True, width=5)
minutes_45 = create_time_keyboard(30, 45, 'minute', forward=True, backward=True, width=5)
minutes_60 = create_time_keyboard(45, 60, 'minute', backward=True, width=5)

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
                                      callback_data=f'{day_en}_week')
    day_week_choice.append(day_button)

day_week_choice_builder = InlineKeyboardBuilder()
day_week_choice_builder.row(*day_week_choice, width=4)
add_base_buttons(day_week_choice_builder, confirm=confirm)
day_week_choice_kb = day_week_choice_builder.as_markup()


