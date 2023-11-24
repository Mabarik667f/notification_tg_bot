from aiogram.fsm.state import StatesGroup


class NotificationFSM(StatesGroup):
    menu_state = 'menu_state'
    get_text_state = 'get_text'
    choice_days_state = 'choice_days'
    week_days_state = 'week_days'
    exact_day_state = 'exact_day'
    year_choice_state = 'year_choice_state'
    month_choice_state = 'month_choice_state'
    day_choice_state = 'day_choice_state'
    hour_choice_state = 'hour_state'
    minute_state = 'minute_state'
    confirm_data_state = 'confirm_data'
    list_note_state = 'list_note'
    date_note_state = 'date_note_state'
    week_note_state = 'week_note_state'
    delete_note_state = 'delete_note_state'
    activate_note_state = 'activate_note_state'
    delete_exact_note_state = 'delete_exact_note_state'
    delete_week_note_state = 'delete_week_note_state'
