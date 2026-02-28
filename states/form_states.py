#states/form_states.py

from aiogram.fsm.state import State, StatesGroup

class FormState(StatesGroup):
    filling = State()
    confirming = State()