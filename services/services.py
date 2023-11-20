from bot import NotificationFSM
from models.methods import get_all_exact_notification_from_db, get_all_week_day_notification_from_db


def create_text(month=None, day=None, hour=None, minute=None):
    date = {}
    if month is not None and day is not None:
        if month < 10:
            month = f"0{month}"

        if day < 10:
            day = f"0{day}"

        date['month'] = month
        date['day'] = day
    if hour is not None and minute is not None:
        if hour < 10:
            hour = f"0{hour}"

        if minute < 10:
            minute = f"0{minute}"

        date['hour'] = hour
        date['minute'] = minute
    return date


async def check_week_day(state, obj) -> None:
    if await state.get_state() in (NotificationFSM.week_days_state,
                                   NotificationFSM.minute_state,
                                   NotificationFSM.hour_choice_state,
                                   NotificationFSM.get_text_state,
                                   NotificationFSM.confirm_data_state):
        obj.days = []
        obj.data = {}


async def get_format_time(time):
    hours, remainder = divmod(time.seconds, 3600)
    minutes = remainder // 60
    time_format = f"{hours:02d}:{minutes:02d}"
    return time_format


async def get_all_exact_notification(user_id):
    notes = await get_all_exact_notification_from_db(user_id)
    notes_data = []
    for note in notes:
        date = note[0].strftime("%Y-%m-%d")
        time = await get_format_time(note[1])
        text, _id = note[2], note[3]
        notes_data.append([date, time, text, _id])

    return notes_data


async def get_all_week_notification(user_id):
    notes, days = await get_all_week_day_notification_from_db(user_id)
    notes_ans = []
    for i in range(len(notes)):
        note = [*notes[i]]
        time = await get_format_time(note[0])
        note[0] = time
        note.append(days[note[-1]])
        notes_ans.append(note)
    return notes_ans
