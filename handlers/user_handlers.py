from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery
from filters.filters import IsTimeCallbackData, IsHourCallbackData

from keyboards.kb_utils import notification_methods_kb, notification_add_kb, hour_choice_am, hour_choice_pm
from lexicon.lexicon import LEXICON, LEXICON_BUTTONS

router = Router()


# Базовые команды или кнопки


@router.message(CommandStart(), StateFilter(default_state))
async def handler_start(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'], reply_markup=notification_methods_kb)


# Раздел с обработкой кнопок и команд для добавления напоминаний


@router.callback_query(F.data == 'add_notification', StateFilter(default_state))
async def handler_callback_add_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/add_notification'],
                                     reply_markup=notification_add_kb)


@router.message(Command(commands='add_notification'), StateFilter(default_state))
async def handler_add_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/add_notification'],
                         reply_markup=notification_add_kb)


@router.callback_query(IsTimeCallbackData())  # Состояние
async def handler_add_fixed_notification(callback: CallbackQuery, state: FSMContext):
    """Добавление напоминания через фиксированное время"""
    await callback.message.edit_text(text=LEXICON['notification_added'],
                                     reply_markup=notification_methods_kb)
    print(callback.data.endswith('_add'))


@router.callback_query(F.data.in_(['custom_add', 'day_add']))  # Состояние
async def handler_custom_add_hour_notification(callback: CallbackQuery, state: FSMContext):
    """Для добавления интервала времени для даты, большей чем день"""
    await callback.message.edit_text(text=LEXICON['custom_notification'],
                                     reply_markup=hour_choice_am)


@router.callback_query(F.data == '>')  # Состояние
async def handler_forward_notification(callback: CallbackQuery, state: FSMContext):
    """Для добавления интервала времени для даты, большей чем день"""
    await callback.message.edit_text(text=LEXICON['custom_notification'],
                                     reply_markup=hour_choice_pm)


@router.callback_query(F.data == '<')  # Состояние
async def handler_backward_notification(callback: CallbackQuery, state: FSMContext):
    """Для добавления интервала времени для даты, большей чем день"""
    await callback.message.edit_text(text=LEXICON['custom_notification'],
                                     reply_markup=hour_choice_am)


@router.callback_query(IsHourCallbackData())
async def handler_custom_add_minutes_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['pick_minutes'])
# Раздел с обработкой кнопок и команд для удаления напоминаний


@router.callback_query(F.data == 'remove_notification', StateFilter(default_state))
async def handler_callback_remove_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/remove_notification'])


@router.message(Command(commands='remove_notification'), StateFilter(default_state))
async def handler_remove_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/remove_notification'])
