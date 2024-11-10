import asyncio
import aiohttp
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}
all_crypto = ['the-open-network', 'notcoin', 'bitcoin', 'ethereum', 'solana', 'cardano']


async def fetch_crypto_data(crypto_name):
    url = f'https://coinstats.app/coins/{crypto_name}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.find_all('div', class_="content__pIDH8")
            for element in elements:
                # Игнорируем элементы с классом "bullMarketPrice__NIHKm"
                price_change_badge = element.find('div', class_="priceChangeBadge__Qa_fk")
                if price_change_badge:
                    span_element = price_change_badge.find('span')
                    side = price_change_badge.find('i', class_='icon-priceUp')
                    if span_element:
                        percentage = span_element.text
                        if percentage != '37%':
                            return crypto_name, side, percentage
                    else:
                        return crypto_name, 'Data not found', 'Data not found'


async def get_all_crypto_data():
    tasks = [fetch_crypto_data(crypto) for crypto in all_crypto]
    results = await asyncio.gather(*tasks)

    return results
