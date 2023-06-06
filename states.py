from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    comment = State()


class Search(StatesGroup):
    search = State()


class RekState(StatesGroup):
    reklama = State()
