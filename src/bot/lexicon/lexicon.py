LEXICON: dict = {
    '/start': 'Привет!',
    '/add_notification': '📆 Чтобы добавить напоминание',
    '/list_notifications': '📒 Список напоминаний',
    '/back': '❌ Назад',
    'unknown': '❌ Не известная команда',
    'back': '❌ Назад',
    'menu': 'Меню',
    'notification_added': '✅ Напоминание установленно',
    'custom_notification': 'Выберете час ⌚, когда будет срабатывать напоминание',
    'pick_minutes': 'Выберете минуту ⌚, когда будет срабатывать напоминание',
    'choice_days': 'Выберите дни недели, в которые должно срабатывать уведомление',
    'choice_month': 'Выберите месяц',
    'choice_year': 'Выберите год',
    'choice_day': 'Выберите день',
    'choice_hour': 'Выберете час ⌚',
    'choice_minute': 'Выберете минуту ⌚',
    'text': 'Добавьте текст для напоминания',
    'write_text': '❌ Неверный формат \n'
                  'Пожалуйста, добавьте текст',
    'confirm_data': 'Проверьте данные выше и нажмите подтвердить',
    'list_note': 'Список ваших напоминаний'
}

LEXICON_BUTTONS: dict = {
    'add_notification': '📆 Добавить напоминание',
    'list_notifications': '📒 Список напоминаний',
    'menu': 'Меню',
    'week_days': 'Дни недели',
    'exact_date': 'Точная дата',
    'confirm': '✅ Подтвердить',
    'date': 'По дате',
    'week': 'По дням',
    'delete': '🗑️ Удалить напоминание',
    'activate': '✏️ Вкл/Выкл напоминание'
}

LEXICON_MENU_COMMANDS = {
    '/start': 'Начать',
    '/add_notification': '📆 Как добавить напоминание',
    '/list_notifications': '📒 Список напоминаний',
}

day_name_ru = {
    'Monday': 'Пн',
    'Tuesday': 'Вт',
    'Wednesday': 'Ср',
    'Thursday': 'Чт',
    'Friday': 'Пт',
    'Saturday': 'Сб',
    'Sunday': 'Вс'
}

days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
# Задаем порядок для каждого дня недели
order_of_days = {day: index for index, day in enumerate(days_of_week)}

month_name_ru = {
    'January': 'Янв',
    'February': 'Фев',
    'March': 'Мар',
    'April': 'Апр',
    'May': 'Май',
    'June': 'Июн',
    'July': 'Июл',
    'August': 'Авг',
    'September': 'Сен',
    'October': 'Окт',
    'November': 'Ноя',
    'December': 'Дек'
}