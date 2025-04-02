from aiogram.dispatcher.filters.state import State, StatesGroup


class UserDataInputting(StatesGroup):
    wait_for_id = State()

class SignalStates(StatesGroup):
    pair = State()
    global_analysis_type = State()
    analysis_type = State()
    trade_time = State()
