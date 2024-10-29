from aiogram.fsm.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    lang = State()
    full_name = State()
    city = State()
    jinsi = State()
    date = State()
    phone = State()

class MessageState(StatesGroup):
    msg = State()

