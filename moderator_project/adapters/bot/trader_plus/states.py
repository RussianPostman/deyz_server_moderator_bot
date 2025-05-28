from aiogram.fsm.state import StatesGroup, State


class AddTraderState(StatesGroup):
    """
    Добавление нового конфига трейдеров
    """
    vait_file = State()
    return_file = State()
    confirm = State()