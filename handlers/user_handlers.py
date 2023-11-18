from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from bot import NotificationFSM
from keyboards.kb_func import DialogCalendar, WeekDayDate
from keyboards.shema import CalendarFactory, WeekDaysFactory
from services.services import create_text
from keyboards.kb_utils import *
from lexicon.lexicon import LEXICON, LEXICON_BUTTONS, day_name_ru, order_of_days
from models.methods import register_user

router = Router()
# Базовые команды или кнопки
wk = WeekDayDate()


@router.message(CommandStart(), StateFilter(any_state))
async def handler_start(message: Message, state: FSMContext):
    register_user(message.from_user.id)
    await message.answer(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    await state.set_state(NotificationFSM.menu_state)


@router.message(Command(commands='menu'), StateFilter(any_state))
async def handler_menu(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    if await state.get_state() in (NotificationFSM.week_days_state,
                                   NotificationFSM.minute_state,
                                   NotificationFSM.hour_choice_state,
                                   NotificationFSM.get_text_state):
        wk.days = []
        wk.data = {}

    await state.set_state(NotificationFSM.menu_state)


@router.callback_query(F.data == 'menu', StateFilter(any_state))
async def handler_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/start'], reply_markup=notification_methods_kb)
    if await state.get_state() in (NotificationFSM.week_days_state,
                                   NotificationFSM.minute_state,
                                   NotificationFSM.hour_choice_state,
                                   NotificationFSM.get_text_state):
        wk.days = []
        wk.data = {}

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


@router.callback_query(WeekDaysFactory.filter(), StateFilter(NotificationFSM.week_days_state))
async def handler_choice_day_week(callback: CallbackQuery, callback_data: WeekDaysFactory):
    try:

        day = [d for d in callback_data][0]
        if day not in wk.days:
            wk.days.append(day_name_ru[day])
            wk.data[day] = True
            wk.days.sort(key=lambda x: order_of_days.get(x, float('inf')))
        text = f"{LEXICON['choice_days']}\n" \
               f"Выбранные дни: {', '.join(map(str, wk.days))}"
        await callback.message.edit_text(text=text,
                                         reply_markup=day_week_choice_kb)
    except TelegramBadRequest:
        await callback.answer()


@router.callback_query(F.data == 'confirm', StateFilter(NotificationFSM.week_days_state))
async def handler_confirm_select_hour(callback: CallbackQuery, state: FSMContext):
    kb = await wk.get_hour()
    text = f"{LEXICON['choice_hour']}\n" \
           f"Выбранные дни: {', '.join(map(str, wk.days))}"
    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.hour_choice_state)


@router.callback_query(WeekDaysFactory.filter(F.hour | (F.hour == 0)), StateFilter(NotificationFSM.hour_choice_state))
async def handler_select_minute_week_day(callback: CallbackQuery,
                                         callback_data: WeekDaysFactory,
                                         state: FSMContext):
    kb = await wk.get_minute(callback_data.hour)
    text = f"{LEXICON['choice_hour']}\n" \
           f"Выбранные дни: {', '.join(map(str, wk.days))}"
    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.minute_state)


@router.callback_query(WeekDaysFactory.filter(F.minute | (F.minute == 0)), StateFilter(NotificationFSM.minute_state))
async def handler_add_text_week_day(callback: CallbackQuery,
                                    callback_data: WeekDaysFactory,
                                    state: FSMContext):
    date = create_text(hour=callback_data.hour, minute=callback_data.minute)
    text = f"Выбранные дни: {', '.join(map(str, wk.days))}\n" \
           f"Время: {date['hour']}:{date['minute']}\n" \
           f"{LEXICON['text']}"
    await callback.message.edit_text(text=text,
                                     reply_markup=base_kb)

    await state.set_state(NotificationFSM.get_text_state)


# Точная дата
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

    date = create_text(callback_data.month, callback_data.day)

    text = f"{LEXICON['choice_hour']}\n" \
           f"Дата события: {date['day']}.{date['month']}." \
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

    date = create_text(callback_data.month, callback_data.day)

    text = f"{LEXICON['choice_minute']}\n" \
           f"Дата события: {date['day']}.{date['month']}." \
           f"{callback_data.year}\n"

    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.minute_state)


@router.callback_query(CalendarFactory.filter(F.minute | (F.minute == 0)), StateFilter(NotificationFSM.minute_state))
async def handler_add_text_for_notification(callback: CallbackQuery,
                                            callback_data: CalendarFactory,
                                            state: FSMContext):
    date = create_text(callback_data.month, callback_data.day, callback_data.hour, callback_data.minute)
    text = f"Дата события: {date['day']}.{date['month']}." \
           f"{callback_data.year}\n" \
           f"Время события: {date['hour']}:{date['minute']}\n" \
           f"\n" \
           f"{LEXICON['text']}"
    await callback.message.edit_text(text=text,
                                     reply_markup=base_kb)

    await state.set_state(NotificationFSM.get_text_state)


# Ожидание текста и добавление в бд
@router.message(F.text, StateFilter(NotificationFSM.get_text_state))
async def handler_added_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['notification_added'],
                         reply_markup=menu_kb)


@router.message(~F.text, StateFilter(NotificationFSM.get_text_state))
async def handler_added_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['write_text'])


# @router.callback_query(F.data._in(['>>', '<<']), StateFilter(NotificationFSM.minute_state))
# async def handler_nav_button_in_select_minute(callback: CallbackQuery):
#     pass

# Раздел с обработкой кнопок и команд для удаления напоминаний

@router.callback_query(F.data == 'remove_notification', StateFilter(NotificationFSM.menu_state))
async def handler_callback_remove_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/list_notifications'])


@router.message(Command(commands='remove_notification'), StateFilter(NotificationFSM.menu_state))
async def handler_remove_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/list_notifications'])
