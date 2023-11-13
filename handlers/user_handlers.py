from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
# from filters.filters import IsTimeCallbackData, IsHourCallbackData, IsMinuteCallbackData, CheckWeekDayCallbackData
from filters.filters import IsDateTimePostfixCallbackData
from bot import NotificationFSM
from services.services import change_curr_note_info
from keyboards.kb_utils import *
from lexicon.lexicon import LEXICON, LEXICON_BUTTONS
from models.methods import register_user

router = Router()


# Базовые команды или кнопки


@router.message(CommandStart(), StateFilter(any_state))
async def handler_start(message: Message, state: FSMContext):
    register_user(message.from_user.id)
    await message.answer(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    await state.set_state(NotificationFSM.menu_state)


@router.message(Command(commands='menu'), StateFilter(any_state))
async def handler_menu(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    await state.set_state(NotificationFSM.menu_state)

    await change_curr_note_info()


@router.callback_query(F.data == 'menu', StateFilter(any_state))
async def handler_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    await state.set_state(NotificationFSM.menu_state)


# Раздел с обработкой кнопок и команд для добавления напоминаний


@router.callback_query(F.data == 'add_notification', StateFilter(NotificationFSM.menu_state))
async def handler_callback_add_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/add_notification'],
                                     reply_markup=hour_choice)

    await state.set_state(NotificationFSM.hour_choice_state)


@router.message(Command(commands='add_notification'), StateFilter(NotificationFSM.menu_state))
async def handler_add_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/add_notification'],
                         reply_markup=hour_choice)

    await state.set_state(NotificationFSM.hour_choice_state)


@router.callback_query(IsDateTimePostfixCallbackData('_hour'), StateFilter(NotificationFSM.hour_choice_state))
async def handler_custom_add_minutes_notification(callback: CallbackQuery, state: FSMContext):
    text = change_curr_note_info(message=LEXICON['pick_minutes'], hour=callback.data)

    await callback.message.edit_text(text=text,
                                     reply_markup=minutes_15)

    await state.set_state(NotificationFSM.minutes_15_state)


@router.callback_query(IsDateTimePostfixCallbackData('_minute'), StateFilter(NotificationFSM.minutes_15_state,
                                                           NotificationFSM.minutes_30_state,
                                                           NotificationFSM.minutes_45_state,
                                                           NotificationFSM.minutes_60_state))
async def handler_choice_date(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(text=LEXICON['choice_days'],
                                     reply_markup=select_days_kb)
    await state.set_state(NotificationFSM.choice_days_state)


@router.callback_query(F.data == '>', StateFilter(NotificationFSM.minutes_15_state,
                                                  NotificationFSM.minutes_30_state,
                                                  NotificationFSM.minutes_45_state))
async def handler_backward_notification(callback: CallbackQuery, state: FSMContext):
    reply_markup: InlineKeyboardMarkup = minutes_15
    curr_state = await state.get_state()
    if curr_state == NotificationFSM.minutes_15_state:
        reply_markup = minutes_30
        await state.set_state(NotificationFSM.minutes_30_state)
    elif curr_state == NotificationFSM.minutes_30_state:
        reply_markup = minutes_45
        await state.set_state(NotificationFSM.minutes_45_state)
    elif curr_state == NotificationFSM.minutes_45_state:
        reply_markup = minutes_60
        await state.set_state(NotificationFSM.minutes_60_state)
    if reply_markup != minutes_15:
        await callback.message.edit_text(text=LEXICON['custom_notification'],
                                         reply_markup=reply_markup)


@router.callback_query(F.data == '<', StateFilter(NotificationFSM.minutes_30_state,
                                                  NotificationFSM.minutes_45_state,
                                                  NotificationFSM.minutes_60_state))
async def handler_backward_notification(callback: CallbackQuery, state: FSMContext):
    """Для добавления интервала времени для даты, большей чем день"""
    reply_markup: InlineKeyboardMarkup = minutes_60
    curr_state = await state.get_state()
    if curr_state == NotificationFSM.minutes_30_state:
        reply_markup = minutes_15
        await state.set_state(NotificationFSM.minutes_15_state)
    elif curr_state == NotificationFSM.minutes_45_state:
        reply_markup = minutes_30
        await state.set_state(NotificationFSM.minutes_30_state)
    elif curr_state == NotificationFSM.minutes_60_state:
        reply_markup = minutes_45
        await state.set_state(NotificationFSM.minutes_45_state)
    if reply_markup != minutes_60:
        await callback.message.edit_text(text=LEXICON['custom_notification'],
                                         reply_markup=reply_markup)


@router.callback_query(F.data == 'week_days', StateFilter(NotificationFSM.choice_days_state))
async def handler_choice_week_days(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['choice_days'],
                                     reply_markup=day_week_choice_kb)
    await state.set_state(NotificationFSM.week_days_state)


@router.callback_query(F.data == 'exact_date', StateFilter(NotificationFSM.choice_days_state))
async def handler_exact_year(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['choice_year'],
                                     reply_markup=choice_year_kb)

    await state.set_state(NotificationFSM.year_choice_state)


@router.callback_query(IsDateTimePostfixCallbackData('_year'), StateFilter(NotificationFSM.year_choice_state))
async def handler_exact_month(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['month_choice'],
                                     reply_markup=choice_month_kb)

    await state.set_state(NotificationFSM.month_choice_state)


# Раздел с обработкой кнопок и команд для удаления напоминаний

@router.callback_query(F.data == 'remove_notification', StateFilter(NotificationFSM.menu_state))
async def handler_callback_remove_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/remove_notification'])


@router.message(Command(commands='remove_notification'), StateFilter(NotificationFSM.menu_state))
async def handler_remove_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/remove_notification'])
