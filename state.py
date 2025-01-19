from aiogram.fsm.state import StatesGroup, State
class UserState(StatesGroup):
    get_start = State()
    get_instruction = State()
