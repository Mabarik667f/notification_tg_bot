from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery
from bot import NotificationFSM
from keyboards.shema import CalendarFactory, WeekDaysFactory
from keyboards.kb_func import DialogCalendar, WeekDayDate, create_confirm_kb, create_exact_note_kb, create_week_note_kb
from services.services import create_text, check_week_day, get_all_week_notification
from keyboards.kb_utils import *
from lexicon.lexicon import LEXICON, day_name_ru, order_of_days
from models.methods import register_user, create_notification, delete_notification, activate_week_notification
from models.redis_methods import save_data_to_redis

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

    await check_week_day(state, wk)

    await state.set_state(NotificationFSM.menu_state)


@router.callback_query(F.data == 'menu', StateFilter(any_state))
async def handler_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/start'], reply_markup=notification_methods_kb)

    await check_week_day(state, wk)

    await state.set_state(NotificationFSM.menu_state)


# Раздел с обработкой кнопок и команд для добавления напоминаний


@router.callback_query(F.data == 'add_notification', StateFilter(NotificationFSM.menu_state))
async def handler_callback_add_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['text'], reply_markup=menu_kb)

    await state.set_state(NotificationFSM.get_text_state)


@router.message(Command(commands='add_notification'), StateFilter(NotificationFSM.menu_state))
async def handler_add_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['text'], reply_markup=menu_kb)

    await state.set_state(NotificationFSM.get_text_state)


@router.message(F.text, StateFilter(NotificationFSM.get_text_state))
async def handler_added_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/add_notification'],
                         reply_markup=select_days_kb)

    await save_data_to_redis(message.from_user.id, message.text)

    await state.set_state(NotificationFSM.choice_days_state)


@router.message(~F.text, StateFilter(NotificationFSM.get_text_state))
async def handler_added_notification(message: Message):
    await message.answer(text=LEXICON['write_text'], reply_markup=menu_kb)


# Работа по дням недели
@router.callback_query(F.data == 'week_days', StateFilter(NotificationFSM.choice_days_state))
async def handler_choice_week_days(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['choice_days'],
                                     reply_markup=day_week_choice_kb)
    await state.set_state(NotificationFSM.week_days_state)


@router.callback_query(WeekDaysFactory.filter(), StateFilter(NotificationFSM.week_days_state))
async def handler_choice_day_week(callback: CallbackQuery, callback_data: WeekDaysFactory):
    try:

        day = [d for d in callback_data][0]
        if day_name_ru[day] not in wk.days:
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
           f"{LEXICON['confirm_data']}"
    kb = create_confirm_kb(callback_data.pack())
    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.confirm_data_state)


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
           f"{LEXICON['confirm_data']}\n"

    kb = create_confirm_kb(callback_data.pack())
    if kb:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.confirm_data_state)


# Добавление в бд

@router.callback_query(CalendarFactory.filter(), StateFilter(NotificationFSM.confirm_data_state))
async def handler_add_notification_to_db(callback: CallbackQuery,
                                         callback_data: CalendarFactory,
                                         state: FSMContext):
    await create_notification(callback.from_user.id, callback_data)

    await callback.message.edit_text(text=LEXICON['notification_added'],
                                     reply_markup=menu_kb)


@router.callback_query(WeekDaysFactory.filter(), StateFilter(NotificationFSM.confirm_data_state))
async def handler_add_notification_to_db(callback: CallbackQuery,
                                         callback_data: CalendarFactory,
                                         state: FSMContext):
    await create_notification(callback.from_user.id, callback_data)

    await callback.message.edit_text(text=LEXICON['notification_added'],
                                     reply_markup=menu_kb)


# Раздел с обработкой кнопок и команд для удаления напоминаний

@router.callback_query(F.data == 'list_notifications', StateFilter(NotificationFSM.menu_state))
async def handler_callback_remove_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['/list_notifications'],
                                     reply_markup=list_notifications_type_kb)

    await state.set_state(NotificationFSM.list_note_state)


@router.message(Command(commands='list_notifications'), StateFilter(NotificationFSM.menu_state))
async def handler_remove_notification(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/list_notifications'],
                         reply_markup=list_notifications_type_kb)

    await state.set_state(NotificationFSM.list_note_state)


@router.callback_query(F.data == 'date', StateFilter(NotificationFSM.list_note_state))
async def handler_list_exact_date_note(callback: CallbackQuery,
                                       state: FSMContext):
    kb = await create_exact_note_kb(callback.from_user.id)
    if kb:
        await callback.message.edit_text(text=LEXICON['list_note'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.date_note_state)


@router.callback_query(F.data == 'week', StateFilter(NotificationFSM.list_note_state))
async def handler_list_week_date_note(callback: CallbackQuery,
                                      state: FSMContext):
    kb = await create_week_note_kb(callback.from_user.id)
    if kb:
        await callback.message.edit_text(text=LEXICON['list_note'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.week_note_state)


@router.callback_query(F.data == 'delete_note', StateFilter(NotificationFSM.date_note_state))
async def handler_exact_delete_note_menu(callback: CallbackQuery, state: FSMContext):
    kb = await create_exact_note_kb(callback.from_user.id, remove=True)
    if kb:
        await callback.message.edit_text(text=LEXICON['list_note'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.delete_exact_note_state)


@router.callback_query(F.data == 'delete_note', StateFilter(NotificationFSM.week_note_state))
async def handler_week_delete_note_menu(callback: CallbackQuery, state: FSMContext):
    kb = await create_week_note_kb(callback.from_user.id, remove=True)
    if kb:
        await callback.message.edit_text(text=LEXICON['list_note'],
                                         reply_markup=kb)

    await state.set_state(NotificationFSM.delete_week_note_state)


@router.callback_query(F.data.endswith('_delete'), StateFilter(NotificationFSM.delete_exact_note_state))
async def handler_delete_one_note_exact(callback: CallbackQuery, state: FSMContext):
    _id = callback.data.split('_')[0]
    await delete_notification(_id)

    await handler_exact_delete_note_menu(callback, state)


@router.callback_query(F.data.endswith('_delete'), StateFilter(NotificationFSM.delete_week_note_state))
async def handler_delete_one_note_week(callback: CallbackQuery, state: FSMContext):
    _id = callback.data.split('_')[0]
    await delete_notification(_id)

    await handler_week_delete_note_menu(callback, state)


@router.callback_query(F.data.endswith('_activate'), StateFilter(NotificationFSM.week_note_state))
async def handler_delete_one_note_week(callback: CallbackQuery, state: FSMContext):
    _id = callback.data.split('_')[0]
    await activate_week_notification(_id)

    await handler_list_week_date_note(callback, state)
