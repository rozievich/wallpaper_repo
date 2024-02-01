from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    comment = State()


class RekState(StatesGroup):
    reklama = State()
