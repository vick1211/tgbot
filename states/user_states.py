from aiogram.fsm.state import State, StatesGroup

class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_post = State()
    fill_grade = State()

class FSMSendMessage(StatesGroup):
    fill_text = State()
    fill_grade = State()