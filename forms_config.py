#forms_config.py

FORMS = {
    "orders": {
        "title": "новый заказ",

        # Лист Google Sheets
        "sheet_name": "orders",

        "send_to_group": True,

        # Автоинкремент ID в колонке A
        "auto_increment_id": {
            "enabled": True,
            "column": "A",
            "start_cell": "A2"
        },

        # Колонки куда записываем ответы
        "columns": [
            "B", "C", "D", "E", "F", "G", "H",
            "I", "J", "K", "L", "M", "N", "O", "R"
        ],

        # Формулы которые копируются из 2 строки
        "formulas": {
            "enabled": True,
            "template_row": 2,
            "columns": ["P", "Q", "S"]
        },

        # Вопросы пользователю (в том же порядке что и columns)
        "questions": [
            {
                "column": "B",
                "text": "Введите дату доставки в формате DD.MM.YYYY:",
                "type": "date"
            },
            {
                "column": "C",
                "text": "Введите время доставки в формате HH:MM:",
                "type": "time"
            },
            {
                "column": "D",
                "text": "Введите имя получателя:",
                "type": "text"
            },
            {
                "column": "E",
                "text": "Введите номер телефона получателя:",
                "type": "text"
            },
            {
                "column": "F",
                "text": "Введите юзернейм получателя:",
                "type": "text"
            },
            {
                "column": "G",
                "text": "Введите адрес получателя:",
                "type": "text"
            },
            {
                "column": "H",
                "text": "Введите товар:",
                "type": "text"
            },
            {
                "column": "I",
                "text": "Введите количество:",
                "type": "number"
            },
            {
                "column": "J",
                "text": "Введите сорт:",
                "type": "dynamic_select",
                "source": "variety"
            },
            {
                "column": "K",
                "text": "Введите цвет:",
                "type": "dynamic_select",
                "source": "color"
            },
            {
                "column": "L",
                "text": "Введите цену за 1 шт:",
                "type": "dynamic_select",
                "source": "price"
            },
            {
                "column": "M",
                "text": "Введите доп пожелания от клиента:",
                "type": "text"
            },
            {
                "column": "N",
                "text": "Введите расход на заказ:",
                "type": "number"
            },
            {
                "column": "O",
                "text": "Введите скидку:",
                "type": "number"
            },
            {
                "column": "R",
                "text": "Введите сколько оплачено:",
                "type": "number"
            },
        ]
    },
    # "supplier": {
    #     "title": "новое поступление",
    #
    #     # Лист Google Sheets
    #     "sheet_name": "supplier",
    #
    #     # Автоинкремент ID в колонке A
    #     "auto_increment_id": {
    #         "enabled": True,
    #         "column": "A",
    #         "start_cell": "A2"
    #     },
    #
    #     # Колонки куда записываем ответы
    #     "columns": [
    #         "B", "C", "D", "E", "F", "G", "H",
    #
    #     ],
    #
    #     # Формулы которые копируются из 2 строки
    #     "formulas": {
    #         "enabled": True,
    #         "template_row": 2,
    #         "columns": ["I"]
    #     },
    #
    #     # Вопросы пользователю (в том же порядке что и columns)
    #     "questions": [
    #         {
    #             "column": "B",
    #             "text": "Введите имя поставщика:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "C",
    #             "text": "Введите дату доставки:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "D",
    #             "text": "Введите сорт:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "E",
    #             "text": "Введите цвет:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "F",
    #             "text": "Введите длину:",
    #             "type": "number"
    #         },
    #         {
    #             "column": "G",
    #             "text": "Введите количество:",
    #             "type": "number"
    #         },
    #         {
    #             "column": "H",
    #             "text": "Введите цену за 1 шт:",
    #             "type": "number"
    #         }
    #     ]
    # },
    # "expenses": {
    #     "title": "новый расход",
    #
    #     # Лист Google Sheets
    #     "sheet_name": "expenses",
    #
    #     # Автоинкремент ID в колонке A
    #     "auto_increment_id": {
    #         "enabled": True,
    #         "column": "A",
    #         "start_cell": "A2"
    #     },
    #
    #     # Колонки куда записываем ответы
    #     "columns": [
    #         "B", "C", "D", "E", "F", "G",
    #     ],
    #
    #     # Формулы которые копируются из 2 строки
    #     "formulas": {
    #         "enabled": True,
    #         "template_row": 2,
    #         "columns": []
    #     },
    #
    #     # Вопросы пользователю (в том же порядке что и columns)
    #     "questions": [
    #         {
    #             "column": "B",
    #             "text": "Введите дату расхода:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "C",
    #             "text": "Введите тип расхода:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "D",
    #             "text": "Введите категорию:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "E",
    #             "text": "Введите подкатегорию:",
    #             "type": "text"
    #         },
    #         {
    #             "column": "F",
    #             "text": "Введите сумму:",
    #             "type": "number"
    #         },
    #         {
    #             "column": "G",
    #             "text": "Введите ответственного:",
    #             "type": "text"
    #         },
    #     ]
    # },
    "income": {
        "title": "новый доход",
        "sheet_name": "income",
        "send_to_group": True,

        "auto_increment_id": {
            "enabled": True,
            "column": "A"
        },

        "questions": [
            {
            "column": "B",
            "text": "Введите дату:",
            "type": "date"
        },
            {
                "column": "C",
                "text": "Выберите order_id:",
                "type": "select_from_sheet",
                "source_sheet": "active_orders",
                "source_column": "A"
            },
            {
                "column": "D",
                "text": "Введите сумму:",
                "type": "select_from_sheet",
                "source_sheet": "active_orders",
                "source_column": "B"
            }
        ]
    }
}
