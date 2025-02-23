from aiogram.fsm.state import StatesGroup, State


class AddAnomalyState(StatesGroup):
    """
    Добавление нового конфига аномалий
    """
    vait_file = State()
    return_file = State()
    confirm = State()