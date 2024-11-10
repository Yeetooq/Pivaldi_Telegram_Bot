from aiogram.fsm.state import State, StatesGroup


class Number(StatesGroup):
    number = State()


class ID(StatesGroup):
    id = State()
    menu = State()
    nazad = State()


class Generate(StatesGroup):
    text = State()


class Registration(StatesGroup):
    name = State()
    number = State()
    location = State()