from aiogram.fsm.state import State, StatesGroup

class FSMBotState(StatesGroup):
    handle_file_state = State()