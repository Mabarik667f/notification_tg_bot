from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, \
    KeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.lexicon import LEXICON, LEXICON_BUTTONS

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
