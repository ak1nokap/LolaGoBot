#handlers/form.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states.form_states import FormState
from core.form_engine import FormEngine

from forms_config import FORMS

router = Router()


@router.callback_query(F.data.startswith("form:"))
async def choose_form(callback: CallbackQuery, state: FSMContext):
    form_key = callback.data.split(":")[1]
    await FormEngine.start_form(callback, state, form_key)
    await callback.answer()


@router.message(FormState.filling)
async def text_answer(message: Message, state: FSMContext):
    await FormEngine.process_text(message, state)


@router.callback_query(FormState.filling, F.data.startswith("opt:"))
async def option_answer(callback: CallbackQuery, state: FSMContext):
    await FormEngine.process_option(callback, state)
    await callback.answer()


@router.callback_query(FormState.confirming, F.data == "confirm")
async def confirm(callback: CallbackQuery, state: FSMContext):
    await FormEngine.confirm(callback, state)
    await callback.answer()


@router.callback_query(FormState.confirming, F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(None)
    await callback.message.answer("❌ Отменено")
    await callback.answer()


@router.callback_query(FormState.filling, F.data.startswith("sheetopt:"))
async def sheet_option_answer(callback: CallbackQuery, state: FSMContext):
    value = callback.data.split(":")[1]

    data = await state.get_data()
    form = FORMS[data["form_key"]]
    step = data["step"]
    question = form["questions"][step]

    data["answers"][question["column"]] = value

    await callback.message.edit_reply_markup(None)
    await FormEngine.next_step(callback.message, state)
    await callback.answer()