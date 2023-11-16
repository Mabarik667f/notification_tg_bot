from lexicon.lexicon import LEXICON
import datetime


def create_text(month, day, hour=None, minute=None):
    if month < 10:
        month = f"0{month}"

    if day < 10:
        day = f"0{day}"
    if hour is not None and minute is not None:
        if hour < 10:
            hour = f"0{hour}"

        if minute < 10:
            minute = f"0{minute}"

    return [month, day, hour, minute]
