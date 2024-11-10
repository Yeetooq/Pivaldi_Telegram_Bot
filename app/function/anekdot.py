import random
import aiohttp
from aiogram.enums import ParseMode
from bs4 import BeautifulSoup
import re
from aiogram import types


async def fetch_anekdot():
    url_1 = "https://anekdotme.ru/random"
    url_2 = "https://anekdotme.ru/luchshie-anekdoti/y_2019/m_4/"
    url_3 = "https://anekdotme.ru/luchshie-anekdoti/y_2017/m_4/"
    url = random.choice([url_1, url_2, url_3])
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"Cache-Control": "no-cache"}) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            anekdots = soup.find_all('div', class_='anekdot_text')
            random_anekdot = random.choice(anekdots).text.strip()
            # Удаление HTML-тегов из анекдота
            random_anekdot = re.sub(r'<[^>]+>', '', random_anekdot)
            return random_anekdot


async def send_anekdot(message: types.Message):
    anekdot = await fetch_anekdot()
    await message.answer(anekdot, parse_mode=ParseMode.HTML)