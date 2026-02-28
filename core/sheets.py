#core/sheets.py

import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_KEY
import re

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SPREADSHEET_KEY)


def get_worksheet(name):
    return spreadsheet.worksheet(name)


def get_headers(sheet_name):
    ws = get_worksheet(sheet_name)
    return ws.row_values(1)


def get_options(sheet_name):
    ws = get_worksheet(sheet_name)
    return ws.col_values(1)


def get_next_id(sheet_name):
    ws = get_worksheet(sheet_name)
    col = ws.col_values(1)
    if len(col) <= 1:
        return 1
    return int(col[-1]) + 1


def save_row(sheet_name, answers_dict, auto_increment):
    ws = get_worksheet(sheet_name)
    next_row = len(ws.get_all_values()) + 1

    if auto_increment:
        new_id = get_next_id(sheet_name)
        ws.update(
            f"A{next_row}",
            [[new_id]],
            value_input_option="USER_ENTERED"
        )

    min_col = min(answers_dict.keys())
    max_col = max(answers_dict.keys())

    start = ord(min_col) - ord("A")
    end = ord(max_col) - ord("A")

    row_data = [""] * (end - start + 1)

    for col_letter, value in answers_dict.items():
        index = ord(col_letter) - ord("A") - start
        row_data[index] = value

    range_name = f"{min_col}{next_row}:{max_col}{next_row}"

    ws.update(
        range_name,
        [row_data],
        value_input_option="USER_ENTERED"
    )
    return next_row


def get_formula_template(sheet_name, template_row, column):
    ws = get_worksheet(sheet_name)
    return ws.acell(
        f"{column}{template_row}",
        value_render_option="FORMULA"
    ).value


def adjust_formula(formula: str, new_row: int):
    # заменяем ВСЕ номера строк на новый номер
    return re.sub(r'(\d+)', str(new_row), formula)


def copy_formulas(sheet_name, formula_config, new_row):
    if not new_row:
        return

    if not formula_config.get("enabled"):
        return

    if not formula_config.get("enabled"):
        return

    template_row = formula_config["template_row"]
    columns = formula_config["columns"]
    ws = get_worksheet(sheet_name)

    for col in columns:
        template_formula = get_formula_template(
            sheet_name,
            template_row,
            col
        )

        if template_formula:
            adjusted = adjust_formula(template_formula, new_row)

            ws.update(
                f"{col}{new_row}",
                [[adjusted]],
                value_input_option="USER_ENTERED"
            )



def get_column_values(sheet_name, column_letter):
    ws = get_worksheet(sheet_name)
    col_index = ord(column_letter) - ord("A") + 1
    values = ws.col_values(col_index)

    # убираем заголовок
    return values[1:]


def is_user_allowed(user_id):
    """
    Проверяет, есть ли user_id в листе 'users' (колонка A)
    """
    ws = get_worksheet("users")
    ids = ws.col_values(2)  # предполагаем, что user_id в колонке A
    return str(user_id) in ids



def get_unique_varieties():
    """
    Возвращает список уникальных сортов (артикулов) из листа storage
    """
    ws = get_worksheet("storage")
    data = ws.get_all_values()[1:]  # пропускаем заголовок

    varieties = list(set(row[3] for row in data if row[3]))
    return sorted(varieties)


def get_colors_by_variety(variety):
    """
    Возвращает список цветов для выбранного сорта
    """
    ws = get_worksheet("storage")
    data = ws.get_all_values()[1:]

    colors = [row[1] for row in data if row[3] == variety]
    return sorted(list(set(colors)))


def get_price_by_variety_and_color(variety, color):
    ws = get_worksheet("storage")
    data = ws.get_all_values()[1:]

    for row in data:
        if row[3] == variety and row[1] == color:
            return row[5]  # колонка F — цена продажи

    return None


def get_storage_info(variety, color, price):
    """
    Возвращает (article, supplier_name)
    из листа storage по сорту, цвету и цене
    """

    ws = get_worksheet("storage")
    data = ws.get_all_values()[1:]  # пропускаем заголовок

    for row in data:
        # ⚠️ индексы подставь если у тебя другие колонки
        # row[3] = сорт
        # row[1] = цвет
        # row[5] = цена
        # row[0] = артикул
        # row[2] = поставщик

        if (
            row[3] == str(variety)
            and row[1] == str(color)
            and row[5] == str(price)
        ):
            article = row[2]
            supplier = row[0]
            photo_id = row[6] if len(row) > 6 else None
            return article, supplier, photo_id

    return None, None, None
