import aiohttp
from bs4 import BeautifulSoup

from app.crypto.all_check import HEADERS


async def fetch_crypto_data(url):
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
                            return side, percentage
                    else:
                        return 'Data not found', 'Data not found'


async def ton():
    return await fetch_crypto_data('https://coinstats.app/coins/the-open-network/')


async def nott():
    return await fetch_crypto_data('https://coinstats.app/coins/notcoin/')


async def eth():
    return await fetch_crypto_data('https://coinstats.app/coins/ethereum/')


async def btc():
    return await fetch_crypto_data('https://coinstats.app/coins/bitcoin/')


async def sol():
    return await fetch_crypto_data('https://coinstats.app/coins/solana/')


async def ada():
    return await fetch_crypto_data('https://coinstats.app/coins/cardano/')