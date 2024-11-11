from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNELS
from app.database.requests import get_categories, get_category_menu

bronirovanie = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Посмотреть места в Pivaldi',
                                           web_app=WebAppInfo(url='https://pivaldi.restoplace.ws/'))]],
    resize_keyboard=True
)

site = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Сайт ресторана Pivaldi',
                                           web_app=WebAppInfo(url='https://pivaldi.ru/'))]],
    resize_keyboard=True
)

kb_weather = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Зеленоград", callback_data='zelenograd'),
                      InlineKeyboardButton(text="Юрлово", callback_data='yurlovo')],
                     [InlineKeyboardButton(text="Одинцово", callback_data='odincovo'),
                      InlineKeyboardButton(text="Мытищи", callback_data='mitishi')]],
    resize_keyboard=True,

)

kb_crypto = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="TON", callback_data='ton'),
                      InlineKeyboardButton(text="NOT", callback_data='not')],
                     [InlineKeyboardButton(text="BTC", callback_data='btc'),
                      InlineKeyboardButton(text="ETH", callback_data='eth')],
                     [InlineKeyboardButton(text="SOL", callback_data='sol'),
                      InlineKeyboardButton(text="ADA", callback_data='ada')],
                     [InlineKeyboardButton(text="stop info ❌", callback_data='stop')]
                     ],
    resize_keyboard=True,
)

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер 📱',
                                                           request_contact=True)]],
                                 resize_keyboard=True)

get_location = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить гео 🗺️',
                                                             request_location=True)]],
                                   resize_keyboard=True)

delete_reg = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Удалить ваши данные ❌',
                                           callback_data='delete_reg')]],
    resize_keyboard=True
)


def showChannels():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[], row_width=1)
    for channel in CHANNELS:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
        keyboard.inline_keyboard.append([btn])  # Append btn as a list
    btnDoneSub = InlineKeyboardButton(text="я подписался ✅", callback_data="subchanneldone")
    keyboard.inline_keyboard.append([btnDoneSub])  # Append btnDoneSub as a list
    return keyboard


async def categories_menu():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='Закрыть меню ❌', callback_data='close_menu'))
    return keyboard.adjust(2).as_markup()


async def nazad():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад ↩️', callback_data='to_nazad'))
    return keyboard.adjust(1).as_markup()


async def nazad_bar():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад ↩️', callback_data='to_main'))
    return keyboard.adjust(1).as_markup()


async def menu(category_id):
    all_menu = await get_category_menu(category_id)
    keyboard = InlineKeyboardBuilder()
    for menu in all_menu:
        keyboard.add(InlineKeyboardButton(text=menu.bludo, callback_data=f"menu_{menu.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную ↩️', callback_data='to_main'))
    return keyboard.adjust(1).as_markup()
