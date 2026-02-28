from datetime import datetime


def parse_date(value: str):
    """
    Возвращает datetime.date или None
    """
    try:
        return datetime.strptime(value, "%d.%m.%Y").date()
    except ValueError:
        return None


def parse_time(value: str):
    """
    Возвращает datetime.time или None
    """
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        return None


def validate_date_not_past(value: str):
    """
    Проверяет:
    - формат
    - дата не в прошлом
    """
    parsed = parse_date(value)

    if not parsed:
        return False, "❌ Неверный формат даты.\nВведите в формате DD.MM.YYYY\nПример: 25.12.2026"

    today = datetime.now().date()

    if parsed < today:
        return False, "❌ Нельзя выбрать прошедшую дату."

    return True, None


def validate_time_not_past(date_str: str, time_str: str):
    """
    Проверяет:
    - формат времени
    - если дата сегодня → время не в прошлом
    """

    parsed_time = parse_time(time_str)
    if not parsed_time:
        return False, "❌ Неверный формат времени.\nВведите в формате HH:MM\nПример: 14:30"

    parsed_date = parse_date(date_str)
    if not parsed_date:
        return False, "Ошибка даты."

    now = datetime.now()

    if parsed_date == now.date():
        selected_datetime = datetime.combine(parsed_date, parsed_time)
        if selected_datetime < now:
            return False, "❌ Нельзя выбрать прошедшее время."

    return True, None