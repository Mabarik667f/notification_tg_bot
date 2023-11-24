import pymysql
from src.config import load_config

cfg = load_config()


def connection_db():
    connection = pymysql.connect(database=cfg.db.database,
                                 user=cfg.db.db_user,
                                 password=cfg.db.db_password,
                                 host=cfg.db.db_host,
                                 port=3306)

    return connection


db = connection_db()
try:
    with db.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DayOfWeek (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            day_name VARCHAR(2) UNIQUE
            )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
        user_id INT PRIMARY KEY
            )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notification (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            notification_time TIME, 
            text VARCHAR(255),
            activate BOOL,
            FOREIGN KEY(user_id) REFERENCES User(user_id)
            )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ExactDate (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            notification_id INT,
            FOREIGN KEY(notification_id) REFERENCES Notification(id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS WeekDayHasNotification (
            week_day_id INT,
            notification_id INT,
            FOREIGN KEY(notification_id) REFERENCES Notification(id) ON DELETE CASCADE,
            FOREIGN KEY(week_day_id) REFERENCES DayOfWeek(id)
            )
        ''')

    with db.cursor() as cursor:
        cursor.execute('''SELECT COUNT(*) FROM DayOfWeek''')
        count = cursor.fetchone()[0]
        day_of_the_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        if count == 0:
            for day in day_of_the_week:
                cursor.execute('INSERT INTO DayOfWeek (day_name) VALUES (%s)', (day,))

    db.commit()

finally:
    db.close()
