from models.models import connection_db


def register_user(user_id):
    db = connection_db()
    try:
        with db.cursor() as cursor:
            user = cursor.execute('SELECT user_id FROM User '
                                  'WHERE user_id = (%s)', (user_id,))
            if not user:
                cursor.execute('INSERT INTO User (user_id) VALUES (%s)', (user_id,))

            db.commit()
    finally:
        db.close()
