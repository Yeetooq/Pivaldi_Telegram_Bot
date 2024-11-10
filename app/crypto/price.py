import asyncio
import aiohttp
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}
all_crypto = ['the-open-network', 'notcoin', 'bitcoin', 'ethereum', 'solana', 'cardano']


async def price(crypto_name):
    url = f'https://coinstats.app/coins/{crypto_name}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.find('div', class_='priceWrapper__KyX8P mainPrice__tM6aY')
            price = data.find('p').text
            return crypto_name, price


async def get_all_crypto_price():
    tasks = [price(crypto) for crypto in all_crypto]
    results = await asyncio.gather(*tasks)

    return results


