from src.bot.keyboards.shema import WeekDaysFactory, CalendarFactory
from src.bot.lexicon.lexicon import day_name_ru
from .models import connection_db
from datetime import datetime
from .redis_methods import get_data_from_redis


def register_user(user_id):
    db = connection_db()
    try:
        with db.cursor() as cursor:
            user = cursor.execute('SELECT user_id FROM user '
                                  'WHERE user_id = (%s)', (user_id,))
            if not user:
                cursor.execute('INSERT INTO user (user_id) VALUES (%s)', (user_id,))

            db.commit()
    finally:
        db.close()


async def create_notification(storage, user_id, callback_data):
    db = connection_db()
    try:
        with db.cursor() as cursor:
            time_str = f"{callback_data.hour}:{callback_data.minute}"
            text = await get_data_from_redis(storage, user_id)
            time = datetime.strptime(time_str, '%H:%M').time()
            sql = 'INSERT INTO notification (user_id, notification_time, text, activate) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql, (user_id, time, text, True))

            inserted_id = cursor.lastrowid

            if isinstance(callback_data, WeekDaysFactory):
                id_days = []
                days = [day_name_ru[day] for day in callback_data]
                for d in days:
                    cursor.execute('SELECT id FROM day_of_week '
                                   'WHERE day_name = %s ', (d,))
                    id_days.append(*cursor.fetchone())

                for _id in id_days:
                    cursor.execute('INSERT INTO week_day_has_notification (week_day_id, notification_id) '
                                   ' VALUES (%s, %s)', (_id, inserted_id))

            elif isinstance(callback_data, CalendarFactory):
                date_str = f"{callback_data.day}.{callback_data.month}.{callback_data.year}"
                date_exact = datetime.strptime(date_str, "%d.%m.%Y")
                sql_exact = 'INSERT INTO exact_date (date, notification_id) VALUES (%s, %s)'
                cursor.execute(sql_exact, (date_exact, inserted_id))

        db.commit()

    finally:
        db.close()


async def get_all_exact_notification_from_db(user_id):
    db = connection_db()

    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT exact_date.date, notification.notification_time, notification.text, notification.id '
                           'FROM notification '
                           'INNER JOIN exact_date ON notification.id = exact_date.notification_id '
                           'WHERE user_id = %s', (user_id,))

        db.commit()

    finally:
        db.close()
        return cursor.fetchall()


async def get_all_week_day_notification_from_db(user_id):
    db = connection_db()
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT notification_time, text, activate, id '
                           'FROM notification '
                           'WHERE user_id = %s', (user_id,))
            notifications = [*cursor.fetchall()]
            days = dict()
            for note in notifications:
                cursor.execute('SELECT day_name FROM day_of_week '
                               'WHERE day_of_week.id IN ( '
                               'SELECT week_day_id FROM week_day_has_notification '
                               'WHERE notification_id = %s) '
                               'ORDER BY day_of_week.id;', (note[-1]))
                days[note[-1]] = []
                for day in cursor.fetchall():
                    days[note[-1]].append(*day)

        db.commit()

    finally:
        db.close()
        return notifications, days


async def delete_notification(_id):
    db = connection_db()
    try:
        with db.cursor() as cursor:
            cursor.execute('DELETE FROM notification WHERE id = %s', (_id,))

        db.commit()

    finally:
        db.close()


async def activate_week_notification(_id):
    db = connection_db()
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT activate FROM notification '
                           'WHERE id = %s', (_id,))

            activate = [*cursor.fetchone()]
            if activate[0]:
                cursor.execute('UPDATE notification SET activate = %s '
                               'WHERE id = %s ', (False, _id))
            else:
                cursor.execute('UPDATE notification SET activate = %s '
                               'WHERE id = %s ', (True, _id))

        db.commit()

    finally:
        db.close()
