
'''
from pycoingecko import CoinGeckoAPI
import time

cg = CoinGeckoAPI()

def get_all_pages(per_page=250, vs_currency='usd'):
    page_num = 1
    all_data = []
    while True:
        data = cg.get_coins_markets(vs_currency=vs_currency, per_page=per_page, page=page_num)
        if not data:
            break
        all_data.extend(data)
        page_num += 1
        time.sleep(1)  # Respect rate limits (e.g., 10-30 calls per minute)
    return all_data

all_coins_data = get_all_pages()
print(f"Total coins fetched: {len(all_coins_data)}")
'''


import pandas as pd
import requests
import requests_cache
import json

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&price_change_percentage=1h%2C24h%2C1y&precision=full"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-ULEXj9kgbnAK2kGvieVgsDBL"
}


requests_cache.install_cache('demo_cache')

response = requests.get(url, headers=headers)

save_json("markets.json", response.json())


print(response.text)