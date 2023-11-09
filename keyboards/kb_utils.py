from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, \
    KeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.lexicon import LEXICON, LEXICON_BUTTONS


def add_base_buttons(keyboard: InlineKeyboardBuilder, *args) -> None:
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_BUTTONS['menu'],
                                                                callback_data='menu'),
                                           InlineKeyboardButton(text=LEXICON['back'],
                                                                callback_data='back')]
    if args:
        if args[0]:
            if args[0].text == '<':
                buttons.insert(0, args[0])
        if args[1]:
            if args[1].text == '>':
                buttons.insert(len(buttons), args[1])
    keyboard.row(*buttons, width=4)


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

def create_move_button(forward: bool = False, backward: bool = False) -> tuple:
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
        callback_data = f"{i}_{time_type}"
        time_ls.append(InlineKeyboardButton(text=text, callback_data=callback_data))

    time_ls_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    time_ls_builder.row(*time_ls, width=width)
    backward_button, forward_button = create_move_button(backward=backward, forward=forward)
    add_base_buttons(time_ls_builder, backward_button, forward_button)
    time_ls_kb = time_ls_builder.as_markup()
    return time_ls_kb


hour_choice = create_time_keyboard(0, 24, 'hour')

minutes_15 = create_time_keyboard(0, 15, 'minute', forward=True, width=5)
minutes_30 = create_time_keyboard(15, 30, 'minute', forward=True, backward=True, width=5)
minutes_45 = create_time_keyboard(30, 45, 'minute', forward=True, backward=True, width=5)
minutes_60 = create_time_keyboard(45, 60, 'minute', backward=True, width=5)
