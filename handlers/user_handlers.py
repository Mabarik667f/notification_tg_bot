from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
# from filters.filters import IsTimeCallbackData, IsHourCallbackData, IsMinuteCallbackData, CheckWeekDayCallbackData
from filters.filters import IsDateTimePostfixCallbackData
from bot import NotificationFSM
from keyboards.kb_func import DialogCalendar
from keyboards.shema import CalendarFactory
from services.services import create_text
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


@router.callback_query(F.data == 'menu', StateFilter(any_state))
async def handler_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    await state.set_state(NotificationFSM.menu_state)


# Раздел с обработкой кнопок и команд для добавления напоминаний


@router.callback_query(F.data == 'add_notification', StateFilter(NotificationFSM.menu_state))
async def handler_callback_add_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/add_notification'],
                                     reply_markup=select_days_kb)

    await state.set_state(NotificationFSM.choice_days_state)


@router.message(Command(commands='add_notification'), StateFilter(NotificationFSM.menu_state))
async def handler_add_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/add_notification'],
                         reply_markup=select_days_kb)

    await state.set_state(NotificationFSM.choice_days_state)


@router.callback_query(F.data == 'week_days', StateFilter(NotificationFSM.choice_days_state))
async def handler_choice_week_days(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['choice_days'],
                                     reply_markup=day_week_choice_kb)
    await state.set_state(NotificationFSM.week_days_state)


@router.callback_query(F.data == 'exact_date', StateFilter(NotificationFSM.choice_days_state))
async def handler_exact_year(callback: CallbackQuery,
                             state: FSMContext):
    dl = DialogCalendar()

    kb = await dl.year_calendar()
    if kb:
        await callback.message.edit_text(text=LEXICON['choice_year'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.year_choice_state)


@router.callback_query(CalendarFactory.filter(F.year), StateFilter(NotificationFSM.year_choice_state))
async def handler_exact_month(callback: CallbackQuery,
                              callback_data: CalendarFactory,
                              state: FSMContext):
    dl = DialogCalendar()
    print(callback_data)
    kb = await dl.get_month(callback_data.year)
    if kb:
        await callback.message.edit_text(text=LEXICON['choice_month'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.month_choice_state)


@router.callback_query(CalendarFactory.filter(F.month), StateFilter(NotificationFSM.month_choice_state))
async def handler_exact_day(callback: CallbackQuery,
                            callback_data: CalendarFactory,
                            state: FSMContext):
    dl = DialogCalendar()

    kb = await dl.get_day(callback_data.year, callback_data.month)
    if kb:
        await callback.message.edit_text(text=LEXICON['choice_day'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.day_choice_state)


@router.callback_query(CalendarFactory.filter(F.day), StateFilter(NotificationFSM.day_choice_state))
async def handler_select_hour_notification(callback: CallbackQuery,
                                           callback_data: CalendarFactory,
                                           state: FSMContext):
    dl = DialogCalendar()

    kb = await dl.get_hour(callback_data.year, callback_data.month, callback_data.day)

    ls = create_text(callback_data.month, callback_data.day)

    text = f"{LEXICON['choice_hour']}\n" \
           f"Дата события: {ls[1]}.{ls[0]}." \
           f"{callback_data.year}\n"
    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.hour_choice_state)


@router.callback_query(CalendarFactory.filter(F.hour | (F.hour == 0)), StateFilter(NotificationFSM.hour_choice_state))
async def handler_select_minute_notification(callback: CallbackQuery,
                                             callback_data: CalendarFactory,
                                             state: FSMContext):
    dl = DialogCalendar()

    kb = await dl.get_minutes(callback_data.year, callback_data.month, callback_data.day, callback_data.hour)

    ls = create_text(callback_data.month, callback_data.day)

    text = f"{LEXICON['choice_hour']}\n" \
           f"Дата события: {ls[1]}.{ls[0]}." \
           f"{callback_data.year}\n"

    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.minute_state)


@router.callback_query(CalendarFactory.filter(F.minute == 59), StateFilter(NotificationFSM.minute_state))
async def handler_add_text_for_notification_minute_59(
        callback: CallbackQuery,
        callback_data: CalendarFactory,
        state: FSMContext):
    dl = DialogCalendar()
    year, month, day, hour, minute = dl.check_time(callback_data.year, callback_data.month, callback_data.day,
                                                   callback_data.hour, callback_data.minute)
    callback_data = CalendarFactory(year=year, month=month, day=day, hour=hour, minute=minute)
    await handler_add_text_for_notification(callback=callback, callback_data=callback_data, state=state)


@router.callback_query(CalendarFactory.filter(F.minute | (F.minute == 0)), StateFilter(NotificationFSM.minute_state))
async def handler_add_text_for_notification(callback: CallbackQuery,
                                            callback_data: CalendarFactory,
                                            state: FSMContext):
    ls = create_text(callback_data.month, callback_data.day, callback_data.hour, callback_data.minute)
    text = f"Дата события: {ls[1]}.{ls[0]}." \
           f"{callback_data.year}\n" \
           f"Время события: {ls[2]}:{ls[3]}\n" \
           f"\n" \
           f"{LEXICON['text']}"
    await callback.message.edit_text(text=text,
                                     reply_markup=base_kb)

    await state.set_state(NotificationFSM.get_text_state)


@router.message(F.text, StateFilter(NotificationFSM.get_text_state))
async def handler_added_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['notification_added'],
                         reply_markup=menu_kb)


@router.message(~F.text, StateFilter(NotificationFSM.get_text_state))
async def handler_added_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['write_text'])


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


# Раздел с обработкой кнопок и команд для удаления напоминаний


@router.callback_query(F.data == 'remove_notification', StateFilter(NotificationFSM.menu_state))
async def handler_callback_remove_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/list_notifications'])


@router.message(Command(commands='remove_notification'), StateFilter(NotificationFSM.menu_state))
async def handler_remove_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/list_notifications'])
