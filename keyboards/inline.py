#keyboards/inline.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def options_keyboard(options):
    keyboard = [
        [InlineKeyboardButton(text=opt, callback_data=f"opt:{opt}")]
        for opt in options
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )


def forms_menu(forms):
    keyboard = [
        [InlineKeyboardButton(text=data["title"], callback_data=f"form:{key}")]
        for key, data in forms.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def dynamic_options_keyboard(options, prefix="opt"):
    keyboard = [
        [InlineKeyboardButton(text=str(opt), callback_data=f"{prefix}:{opt}")]
        for opt in options
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)