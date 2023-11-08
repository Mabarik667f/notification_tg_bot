from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, \
    KeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.lexicon import LEXICON, LEXICON_BUTTONS


def add_base_buttons(buttons: list[InlineKeyboardButton]) -> None:
    buttons.append(InlineKeyboardButton(text=LEXICON['back'],
                                        callback_data='back'))


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
add_base_buttons(notification_add)
notification_add_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
notification_add_builder.row(*notification_add, width=3)
notification_add_kb = notification_add_builder.as_markup()


# клавиатура часов

def create_move_button(buttons, forward: bool = False, backward: bool = False) -> None:
    if backward:
        buttons.append(InlineKeyboardButton(text=LEXICON_BUTTONS['backward'],
                                            callback_data=LEXICON_BUTTONS['backward']))
    if forward:
        buttons.append(InlineKeyboardButton(text=LEXICON_BUTTONS['forward'],
                                            callback_data=LEXICON_BUTTONS['forward']))


def create_time_keyboard(j: int, k: int, time_type: str, forward: bool = False,
                         backward: bool = False) -> InlineKeyboardMarkup:
    time_ls: list[InlineKeyboardButton] = []
    for i in range(j, k):
        text = i
        callback_data = f"{i}_{time_type}"
        time_ls.append(InlineKeyboardButton(text=text, callback_data=callback_data))

    add_base_buttons(time_ls)
    create_move_button(time_ls, forward, backward)
    time_ls_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    time_ls_builder.row(*time_ls, width=3)
    time_ls_kb = time_ls_builder.as_markup()
    return time_ls_kb


hour_choice_am = create_time_keyboard(0, 12, 'hour', forward=True)
hour_choice_pm = create_time_keyboard(12, 24, 'hour', backward=True)
