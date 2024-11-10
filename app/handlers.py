import asyncio
import datetime
import json
import numpy as np
import random
import requests
import aiocache
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery, LabeledPrice, InputMediaPhoto, ReplyKeyboardRemove
from geopy.geocoders import Nominatim

from app.crypto.function_crypto import ton, nott, btc, eth, sol, ada
from app.function.check_sub_channels import check_sub_channels
from app.function.anekdot import send_anekdot
from app.crypto.all_check import get_all_crypto_data
from app.crypto.price import get_all_crypto_price
from app.database.requests import (get_category_menu, get_lyudi, update_user_stats, get_user_win, get_user_lose,
                                   calculate_win_percentage)
import app.keyboards as kb
import app.prices as pr
from app.states import Number, Registration
import config
import app.database.requests as rq
from config import API

router = Router()

bot = Bot(token=config.TOKEN)

user_data = {}


@router.message(CommandStart())
async def start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer('Привет 👋\nХочешь вкусно поесть в Pivaldi? 😋\nДавай посмотрим свободные места!',
                         reply_markup=kb.bronirovanie)


@router.message(Command('help'))
async def help(message: types.Message):
    await message.answer('По техническим вопросам обращайтесь сюда @y7t7q7')


@router.message(Command('help_pro'))
async def help_pro(message: types.Message):
    await message.answer('По вопросам обслуживания:\n\nРесторан «PIVALDI» Зеленоград\nТел.: +7(495)477-55-00 '
                         '📞\n\nРесторан «PIVALDI» Одинцово\nТел.: +7(495)477-95-00 📞\n\nРесторан «PIVALDI» '
                         'Юрлово\nТел.: +7(495)477-47-00 📞')


@router.message(Command('website'))
async def website(message: types.Message):
    await message.answer('Наш сайт: <b><a href="https://pivaldi.ru">Pivaldi.ru</a></b>', parse_mode="html")


@router.message(Command('anekdot'))
async def send_random_anekdot(message: types.Message):
    if await check_sub_channels(bot, channels=config.CHANNELS, user_id=message.from_user.id):
        await send_anekdot(message)
    else:
        await message.answer(config.NOT_SUB_MESSAGE, reply_markup=kb.showChannels())


@router.message(Command('pay'))
async def order(message: types.Message, bot: Bot):
    total_amount = sum(price.amount for price in pr.total)

    # Вычисляем максимальные чаевые как 20% от общей суммы заказа
    max_tip_amount = int(total_amount * 0.20)
    tip_amount = int(total_amount)

    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Оплата заказа',
        description='Будьте любезны пополнить казну Pivaldi 😉',
        payload='info for me',
        provider_token='your provider token',
        currency='rub',
        prices=[
            LabeledPrice(
                label='Черри бургер',
                amount=200 * 100
            ),
            LabeledPrice(
                label='Латте',
                amount=0
            ),
            LabeledPrice(
                label='Кокосовый сироп',
                amount=30 * 100
            ),
            LabeledPrice(
                label='Тархун 300мл',
                amount=300 * 100
            ),
            LabeledPrice(
                label='Азиатский салат с угрём',
                amount=200 * 100
            ),
            LabeledPrice(
                label='Скидка постоянного клиента',
                amount=-200 * 100
            )
        ],
        max_tip_amount=max_tip_amount,
        suggested_tip_amounts=[int(tip_amount * 0.05), int(tip_amount * 0.1), int(tip_amount * 0.15),
                               int(tip_amount * 0.2)],
        photo_url='https://pivaldi.ru/wp-content/uploads/2022/04/pivo-glavnaya1.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        allow_sending_without_reply=True,
        request_timeout=15
    )


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: types.Message, bot: Bot):
    chat_id = 'your chat_id without'' '
    total_label = [name.label for name in pr.total]
    # Формирование сообщения об успешной оплате
    msg = (f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}'
           f'\nОжидайте ваш заказ ⏳')
    msg_full = message.successful_payment.order_info
    # Отправка сообщения об успешной оплате
    await message.answer(msg)
    # Отправка сообщения с тем же текстом пользователю с chat_id
    await bot.send_message(chat_id,
                           f'Посетитель по имени {msg_full.name} сделал заказ.\nНомер телефона: {msg_full.phone_number}'
                           f'\nНик в tg: @{message.from_user.username}\n\nЗаказ:\n{", ".join(total_label[:-1])}')


@router.message(Command('weather'))
async def weather(message: types.Message):
    await message.answer('Узнайте погоду перед походом в ресторан, чтобы ничто не помешало вашим планам 🌤️',
                         reply_markup=kb.kb_weather)


@router.message(Command('secret'))
async def command_start_handler(message: types.Message):
    await message.answer(
        f"/price - The price of the crypto at the moment 💲\n/check - Check the price change cryptocurrency in the last "
        f"hour 📊\n/nonstop_check - Сryptocurrency change in 1 hour every 3 seconds ⏳")


@router.message(Command('check'))
async def command_check_handler(message: types.Message):
    results = await get_all_crypto_data()
    await message.answer(f"Price change in 1 hour 📊")
    for crypto_name, side, percentage in results:
        if crypto_name == 'the-open-network':
            crypto_name = 'TON'
        if crypto_name == 'notcoin':
            crypto_name = 'NOT'
        if crypto_name == 'bitcoin':
            crypto_name = 'BTC'
        if crypto_name == 'cardano':
            crypto_name = 'ADA'
        if crypto_name == 'solana':
            crypto_name = 'SOL'
        if crypto_name == 'ethereum':
            crypto_name = 'ETH'
        if side:
            await message.answer(f"{crypto_name}: 📈 + {percentage}")
        else:
            await message.answer(f"{crypto_name}: 📉 - {percentage}")


@router.message(Command('price'))
async def command_price_handler(message: types.Message):
    results = await get_all_crypto_price()
    await message.answer(f"The current price of the crypto 💲")
    crpt = {}
    for crypto_name, price in results:
        if crypto_name == 'the-open-network':
            crypto_name = 'TON'
        if crypto_name == 'notcoin':
            crypto_name = 'NOT'
        if crypto_name == 'bitcoin':
            crypto_name = 'BTC'
        if crypto_name == 'cardano':
            crypto_name = 'ADA'
        if crypto_name == 'solana':
            crypto_name = 'SOL'
        if crypto_name == 'ethereum':
            crypto_name = 'ETH'
        crpt[crypto_name] = price
    message_text = "\n\n".join([f"{crypto_name}: {price}" for crypto_name, price in crpt.items()])
    await message.answer(message_text)


@router.message(Command('nonstop_check'))
async def command_nonstop_handler(message: types.Message):
    await message.answer("Select a cryptocurrency to track (every 3 seconds🕒):", reply_markup=kb.kb_crypto)


@router.callback_query(lambda c: c.data in ['ton', 'not', 'btc', 'eth', 'sol', 'ada'])
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    global running
    running = True  # Установить флаг в True
    while running:
        side = percentage = 'Unknown'
        if callback_query.data == 'ton':
            side, percentage = await ton()
        elif callback_query.data == 'not':
            side, percentage = await nott()
        elif callback_query.data == 'btc':
            side, percentage = await btc()
        elif callback_query.data == 'eth':
            side, percentage = await eth()
        elif callback_query.data == 'sol':
            side, percentage = await sol()
        elif callback_query.data == 'ada':
            side, percentage = await ada()

        if side:
            await bot.send_message(callback_query.from_user.id, f"📈 + {percentage}")
        else:
            await bot.send_message(callback_query.from_user.id, f"📉 - {percentage}")

        await asyncio.sleep(3)


@router.callback_query(lambda c: c.data == 'stop')
async def command_stop_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    global running
    running = False  # Установить флаг в False
    await bot.send_message(callback_query.from_user.id, f"Nonstop check has been stopped.")


@router.callback_query(F.data == "zelenograd")
async def zel(callback: types.CallbackQuery):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Зеленоград&appid={API}&units=metric&lang=ru')
    data = json.loads(res.text)
    description = data['weather'][0]['description']
    if data['main']['temp'] > 0.0:
        temp = '+' + str(round(data['main']['temp'])) + '°C' + ', '
    else:
        temp = str(round(data['main']['temp'])) + '°C'
    await callback.answer()
    res_vvv = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?q=Зеленоград&appid={API}&units=metric&lang=ru')
    data_vvv = json.loads(res_vvv.text)
    vvv = np.array([])
    for i in np.arange(4):
        vremya = data_vvv['list'][i]['dt']
        dt = datetime.datetime.fromtimestamp(vremya)
        formatted_time = dt.strftime('%Y-%m-%d | %H:%M')
        if data_vvv['list'][i]['main']['temp'] > 0.0:
            temp_vvv = '+' + str(round(data_vvv['list'][i]['main']['temp'])) + '°C' + ', '
        else:
            temp_vvv = str(round(data_vvv['list'][i]['main']['temp'])) + '°C'

        description_vvv = data_vvv["list"][i]["weather"][0]["description"]
        vvv = np.append(vvv, f'{formatted_time}:' + '\n' + temp_vvv + description_vvv)
    await callback.message.answer(
        'Сейчас в Зеленограде:\n' + temp + description + '\n\nПрогноз на ближайшее время:\n\n'
        + vvv[0] + '\n\n' + vvv[1] + '\n\n' + vvv[2])


@router.callback_query(F.data == "yurlovo")
async def yurl(callback: types.CallbackQuery):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Юрлово&appid={API}&units=metric&lang=ru')
    data = json.loads(res.text)
    description = data['weather'][0]['description']
    if data['main']['temp'] > 0.0:
        temp = '+' + str(round(data['main']['temp'])) + '°C' + ', '
    else:
        temp = str(round(data['main']['temp'])) + '°C'

    await callback.answer()

    res_vvv = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?q=Юрлово&appid={API}&units=metric&lang=ru')
    data_vvv = json.loads(res_vvv.text)
    vvv = np.array([])
    for i in np.arange(4):
        vremya = data_vvv['list'][i]['dt']
        dt = datetime.datetime.fromtimestamp(vremya)
        formatted_time = dt.strftime('%Y-%m-%d | %H:%M')
        if data_vvv['list'][i]['main']['temp'] > 0.0:
            temp_vvv = '+' + str(round(data_vvv['list'][i]['main']['temp'])) + '°C' + ', '
        else:
            temp_vvv = str(round(data_vvv['list'][i]['main']['temp'])) + '°C'

        description_vvv = data_vvv["list"][i]["weather"][0]["description"]
        vvv = np.append(vvv, f'{formatted_time}:' + '\n' + temp_vvv + description_vvv)
    await callback.message.answer(
        'Сейчас в Юрлово:\n' + temp + description + '\n\nПрогноз на ближайшее время:\n\n' + vvv[0] + '\n\n'
        + vvv[1] + '\n\n' + vvv[2])


@router.callback_query(F.data == "odincovo")
async def odinc(callback: types.CallbackQuery):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Одинцово&appid={API}&units=metric&lang=ru')
    data = json.loads(res.text)
    description = data['weather'][0]['description']
    if data['main']['temp'] > 0.0:
        temp = '+' + str(round(data['main']['temp'])) + '°C' + ', '
    else:
        temp = str(round(data['main']['temp'])) + '°C'
    await callback.answer()
    res_vvv = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?q=Одинцово&appid={API}&units=metric&lang=ru')
    data_vvv = json.loads(res_vvv.text)
    vvv = np.array([])
    for i in np.arange(4):
        vremya = data_vvv['list'][i]['dt']
        dt = datetime.datetime.fromtimestamp(vremya)
        formatted_time = dt.strftime('%Y-%m-%d | %H:%M')
        if data_vvv['list'][i]['main']['temp'] > 0.0:
            temp_vvv = '+' + str(round(data_vvv['list'][i]['main']['temp'])) + '°C' + ', '
        else:
            temp_vvv = str(round(data_vvv['list'][i]['main']['temp'])) + '°C'

        description_vvv = data_vvv["list"][i]["weather"][0]["description"]
        vvv = np.append(vvv, f'{formatted_time}:' + '\n' + temp_vvv + description_vvv)
    await callback.message.answer(
        'Сейчас в Одинцово:\n' + temp + description + '\n\nПрогноз на ближайшее время:\n\n' + vvv[0] + '\n\n' + vvv[1]
        + '\n\n' + vvv[2])


@router.callback_query(F.data == "mitishi")
async def mitish(callback: types.CallbackQuery):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Мытищи&appid={API}&units=metric&lang=ru')
    data = json.loads(res.text)
    description = data['weather'][0]['description']
    if data['main']['temp'] > 0.0:
        temp = '+' + str(round(data['main']['temp'])) + '°C' + ', '
    else:
        temp = str(round(data['main']['temp'])) + '°C'
    await callback.answer()
    res_vvv = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?q=Мытищи&appid={API}&units=metric&lang=ru')
    data_vvv = json.loads(res_vvv.text)
    vvv = np.array([])
    for i in np.arange(4):
        vremya = data_vvv['list'][i]['dt']
        dt = datetime.datetime.fromtimestamp(vremya)
        formatted_time = dt.strftime('%Y-%m-%d | %H:%M')
        if data_vvv['list'][i]['main']['temp'] > 0.0:
            temp_vvv = '+' + str(round(data_vvv['list'][i]['main']['temp'])) + '°C' + ', '
        else:
            temp_vvv = str(round(data_vvv['list'][i]['main']['temp'])) + '°C'

        description_vvv = data_vvv["list"][i]["weather"][0]["description"]
        vvv = np.append(vvv, f'{formatted_time}:' + '\n' + temp_vvv + description_vvv)
    await callback.message.answer(
        'Сейчас в Мытищах:\n' + temp + description + '\n\nПрогноз на ближайшее время:\n\n' + vvv[0] + '\n\n' + vvv[1]
        + '\n\n' + vvv[2])


@router.message(Command('catalog'))
async def catalog(message: types.Message):
    # Используем id пользователя для создания ключа в словаре user_data
    user_id = message.from_user.id
    user_data[user_id] = aiocache.SimpleMemoryCache()

    await message.answer('Выберите категорию меню 🛒', reply_markup=await kb.categories_menu())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    category_id = callback.data.split('_')[1]
    # Получаем id пользователя
    user_id = callback.from_user.id
    # Проверяем, есть ли у пользователя переменная data, если нет, создаем новую
    if user_id not in user_data:
        user_data[user_id] = aiocache.SimpleMemoryCache()
    # Сохраняем category_id в переменной data конкретного пользователя
    await user_data[user_id].set('category_id', category_id)
    await callback.answer('')
    if category_id != '13':
        await callback.message.answer('Выберите кухню по категории 🍽️',
                                      reply_markup=await kb.menu(callback.data.split('_')[1]))
    else:
        photki = await get_category_menu(callback.data.split('_')[1])
        # Предполагается, что у вас есть список URL фотографий
        media_group = [InputMediaPhoto(media=photo.photo_url) for photo in photki]

        # Отправить группу фотографий
        await bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_group
        )

        # Ответить на сообщение с кнопкой "Назад в меню"
        await callback.message.answer('Назад в меню ↓', reply_markup=await kb.nazad_bar())


@router.callback_query(F.data.startswith('menu_'))
async def menu(callback: types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    menu_data = await rq.get_menu(callback.data.split('_')[1])
    await callback.answer('')
    if len(menu_data.description) > 1:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=menu_data.photo_url,  # Предполагается, что у вас есть URL фотографии
            caption=f'Название: {menu_data.bludo}\nОписание: {menu_data.description}\nЦена: {menu_data.price} руб.',
            reply_markup=await kb.nazad()
        )
    else:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=menu_data.photo_url,  # Предполагается, что у вас есть URL фотографии
            caption=f'Название: {menu_data.bludo}\nЦена: {menu_data.price} руб.',
            reply_markup=await kb.nazad()
        )


@router.callback_query(lambda c: c.data == 'to_nazad' or c.data == 'to_main' or c.data == 'close_menu')
async def nazad(callback: types.CallbackQuery):
    if callback.data == 'to_nazad':
        # Получаем id пользователя
        user_id = callback.from_user.id
        # Проверяем, есть ли у пользователя переменная data
        if user_id in user_data:
            # Получаем значение category_id из асинхронной переменной data конкретного пользователя
            category_id = await user_data[user_id].get('category_id')
            if category_id:
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
                await callback.message.answer('Выберите кухню по категории 🍽️',
                                              reply_markup=await kb.menu(category_id))
    elif callback.data == 'to_main':
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await catalog(callback.message)
    elif callback.data == 'close_menu':
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@router.callback_query(F.data == "subchanneldone")
async def subchanneldone(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if await check_sub_channels(bot, channels=config.CHANNELS, user_id=callback_query.from_user.id):
        await send_anekdot(callback_query.message)
    else:
        await callback_query.message.answer(config.NOT_SUB_MESSAGE_POVTORNO, reply_markup=kb.showChannels())


@router.message(Command('statistics'))
async def send_welcome(message: types.Message):
    # Получаем значения с помощью ожидания
    wins = await get_user_win(tg_id=message.from_user.id)
    loses = await get_user_lose(tg_id=message.from_user.id)
    win_rate = await calculate_win_percentage(tg_id=message.from_user.id)

    # Формируем сообщение
    await message.answer(f"Ваша статистика игры:\n\n"
                         f"🏆Победы: {wins}\n"
                         f"❌Поражения: {loses}\n"
                         f"📈Win Rate: {win_rate}%")


@router.message(Command('registration'))
async def reg_1(message: types.Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer("Ну что, давай знакомится 👋")
    await message.answer("Как тебя зовут? 👤")


@router.message(Registration.name)
async def reg_2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.number)
    await message.answer('Оставь свой номер телефона 📞', reply_markup=kb.get_number)


@router.message(Registration.number)
async def reg_3(message: types.Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await state.set_state(Registration.location)
    await message.answer('Оставь свою геолокацию 🚩\n***не парься, я не ФСБ***', reply_markup=kb.get_location)


@router.message(Registration.location)
async def reg_final(message: types.Message, state: FSMContext):
    geolocator = Nominatim(user_agent=str(message.from_user.id))
    latitude = message.location.latitude
    longitude = message.location.longitude
    # Преобразуем координаты в адрес
    location = geolocator.reverse((latitude, longitude))
    address = location.address
    await state.update_data(location=address)
    data = await state.get_data()
    await rq.set_reg(message.from_user.id, data["name"], data["number"], data["location"])
    await message.answer('Данные сохранены ✅', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Ваше имя: {data["name"]}\nВаш номер телефона: {data["number"]}'
                         f'\nВаша локация: {data["location"]}', reply_markup=kb.delete_reg)
    await state.clear()


@router.callback_query(F.data == "delete_reg")
async def nah_reg(callback: types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await rq.delete_info(callback.from_user.id)
    await callback.answer()
    await callback.message.answer('Ваша информация удалена безвозвратно ✅')


@router.message(lambda message: message.chat.id == 633542711 and message.text.startswith("Новость: "))
async def forward_news_to_others(message: types.Message):
    # Получаем список всех пользователей из базы данных, которым нужно отправить новость
    result = await get_lyudi()  # Здесь нужно заменить на ваш метод получения пользователей из базы данных
    users = result.fetchall()  # Получаем всех пользователей
    news_text = message.text[len("Новость: "):].strip()  # Удаляем фразу "Новость," и обрезаем пробелы
    for user in users:
        chat_id = user  # Здесь нужно заменить на соответствующий атрибут или индекс, содержащий chat_id
        if chat_id != message.chat.id:  # Убедимся, что мы не отправляем сообщение обратно в источник
            await bot.send_message(chat_id, f"Новость от разработчика: {news_text}")


@router.message(Command('game'))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state(Number.number)
    await message.answer("Я загадал число от 1 до 10 🎲\nПопробуй угадать!")


@router.message(Number.number)
async def guess_number(message: types.Message, state: FSMContext):
    await state.update_data(number=int(message.text))
    secret_number = random.randint(1, 10)
    user_number = int(message.text)

    if user_number == secret_number:
        await update_user_stats(tg_id=message.from_user.id, win=True)
        await message.answer("Поздравляю! Ты угадал число!\nЗаново: /game")
    elif user_number < secret_number:
        await update_user_stats(tg_id=message.from_user.id, win=False)
        await message.answer("Загаданное число было больше(\nЗаново: /game")
    else:
        await update_user_stats(tg_id=message.from_user.id, win=False)
        await message.answer("Загаданное число было меньше(\nЗаново: /game")

    await state.clear()
