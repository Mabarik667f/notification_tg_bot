from lexicon.lexicon import LEXICON
import datetime


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