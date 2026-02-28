# core/form_config.py

from forms_config import FORMS
from core.sheets import get_headers, get_options, save_row, save_row, copy_formulas, get_column_values, \
    get_unique_varieties, get_colors_by_variety, get_price_by_variety_and_color, get_storage_info, get_next_id
from keyboards.inline import options_keyboard, confirm_keyboard, dynamic_options_keyboard
from config import GROUP_CHAT_ID
from core.validators import (
    validate_date_not_past,
    validate_time_not_past,
)


class FormEngine:

    @staticmethod
    async def start_form(callback, state, form_key):
        form = FORMS[form_key]
        await state.update_data(
            form_key=form_key,
            step=0,
            answers={}
        )
        await state.set_state("FormState:filling")
        await callback.message.answer(form["title"])
        await FormEngine.ask_question(callback.message, state)

    @staticmethod
    async def ask_question(message, state):
        data = await state.get_data()
        form = FORMS[data["form_key"]]
        step = data["step"]

        question = form["questions"][step]

        # 🔥 БЕРЕМ ВОПРОС ИЗ CONFIG
        question_text = question["text"]
        if question["type"] == "select_from_sheet":
            options = get_column_values(
                question["source_sheet"],
                question["source_column"]
            )

            await message.answer(
                question_text,
                reply_markup=dynamic_options_keyboard(options, prefix="sheetopt")
            )
        elif question["type"] == "select":
            options = get_options(question["options_sheet"])
            await message.answer(
                question_text,
                reply_markup=options_keyboard(options)
            )

        elif question["type"] == "dynamic_select":

            if question["source"] == "variety":
                options = get_unique_varieties()

            elif question["source"] == "color":
                data_state = await state.get_data()
                selected_variety = data_state["answers"].get("J")
                options = get_colors_by_variety(selected_variety)
            elif question["source"] == "price":
                data_state = await state.get_data()
                selected_variety = data_state["answers"].get("J")
                selected_color = data_state["answers"].get("K")

                price = get_price_by_variety_and_color(
                    selected_variety,
                    selected_color
                )
                options = [price] if price else ["Нет цены"]

            await message.answer(
                question_text,
                reply_markup=options_keyboard(options)
            )
        else:
            await message.answer(question_text)

    @staticmethod
    async def process_text(message, state):
        data = await state.get_data()
        form = FORMS[data["form_key"]]
        step = data["step"]
        question = form["questions"][step]

        value = message.text.strip()

        # --- ЧИСЛО ---
        if question["type"] == "number":
            try:
                value = int(value)
            except:
                await message.answer("❌ Введите число")
                return

        # --- ДАТА ---
        if question["type"] == "date":
            valid, error = validate_date_not_past(value)
            if not valid:
                await message.answer(error)
                return

        # --- ВРЕМЯ ---
        if question["type"] == "time":

            # ищем колонку с датой
            date_column = None
            for q in form["questions"]:
                if q["type"] == "date":
                    date_column = q["column"]
                    break

            selected_date = data["answers"].get(date_column)

            if not selected_date:
                await message.answer("Сначала выберите дату")
                return

            valid, error = validate_time_not_past(selected_date, value)
            if not valid:
                await message.answer(error)
                return

        # --- СОХРАНЕНИЕ ---
        data["answers"][question["column"]] = value
        await state.update_data(answers=data["answers"])

        await FormEngine.next_step(message, state)

    @staticmethod
    async def process_option(callback, state):
        value = callback.data.split(":")[1]

        data = await state.get_data()
        form = FORMS[data["form_key"]]
        step = data["step"]
        question = form["questions"][step]

        data["answers"][question["column"]] = value

        await state.update_data(answers=data["answers"])

        await callback.message.edit_reply_markup(None)
        await FormEngine.next_step(callback.message, state)

    @staticmethod
    async def next_step(message, state):
        data = await state.get_data()
        form = FORMS[data["form_key"]]
        step = data["step"] + 1

        if step < len(form["questions"]):
            await state.update_data(step=step)
            await FormEngine.ask_question(message, state)
        else:
            await state.set_state("FormState:confirming")
            await FormEngine.show_summary(message, state)

    @staticmethod
    async def show_summary(message, state):
        data = await state.get_data()
        form = FORMS[data["form_key"]]
        headers = get_headers(form["sheet_name"])

        lines = []
        for col, val in data["answers"].items():
            index = ord(col) - ord("A")
            lines.append(f"{headers[index]}: {val}")

        text = "\n".join(lines)

        await message.answer(
            f"Проверьте данные:\n\n{text}",
            reply_markup=confirm_keyboard()
        )

    @staticmethod
    async def confirm(callback, state):
        data = await state.get_data()
        form = FORMS[data["form_key"]]

        sheet_name = form["sheet_name"]

        # 🔥 Сохраняем строку
        new_row = save_row(
            sheet_name,
            data["answers"],
            form["auto_increment_id"]["enabled"]
        )

        # 🔥 Копируем формулы если включены
        if form.get("formulas"):
            copy_formulas(
                sheet_name,
                form["formulas"],
                new_row
            )

        # --- Получаем order_id если автоинкремент включен ---
        order_id = None
        if form["auto_increment_id"]["enabled"]:
            order_id = get_next_id(sheet_name) - 1

        # --- Получаем данные пользователя ---
        variety = data["answers"].get("J")
        color = data["answers"].get("K")
        price = data["answers"].get("L")

        article, supplier, photo_id = get_storage_info(variety, color, price)

        # --- Формируем текст саммари ---
        headers = get_headers(sheet_name)
        lines = []

        for col, val in data["answers"].items():
            index = ord(col) - ord("A")
            lines.append(f"{headers[index]}: {val}")

        text = "\n".join(lines)

        extra_info = ""
        if article:
            extra_info += f"\nАртикул: {article}"
        if supplier:
            extra_info += f"\nПоставщик: {supplier}"

        summary_text = f"📌 {form['title'].capitalize()}\n"
        if order_id:
            summary_text += f"ID: {order_id}\n\n"
        summary_text += f"{text}{extra_info}"

        # --- ОТПРАВКА В ГРУППУ, если нужно ---
        if form.get("send_to_group"):
            sent_message = await callback.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=summary_text
            )

            if photo_id:
                await callback.bot.send_photo(
                    chat_id=GROUP_CHAT_ID,
                    photo=photo_id,
                    reply_to_message_id=sent_message.message_id
                )

            await callback.message.answer("✅ Запись сохранена и отправлена в группу")
        else:
            await callback.message.answer("✅ Запись сохранена")

        await state.clear()
