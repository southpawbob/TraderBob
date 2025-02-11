import requests
import requests_cache
import json
import time
import pandas as pd
from bokeh.plotting import curdoc, show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
import sys
import decimal

#session = CachedSession('demo_cache', cache_control=True)
#session = CachedSession('demo_cache', )
requests_cache.install_cache('cache')

def convert_numbers_to_strings(obj):
    if isinstance(obj, float):
        return str(obj)
    return obj

def fetch_all_markets():

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&sparkline=true&price_change_percentage=1h%2C24h%2C7d%2C14d%2C30d%2C200d%2C1y&precision=full"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-ULEXj9kgbnAK2kGvieVgsDBL"
    }
    page_num = 1
    dfAll = pd.DataFrame();
    all_data = []
    while True:
        params = {"page": page_num}
        response = requests.get(url, headers=headers, params=params)
        print("request page: ", page_num)
        data = json.loads(response.text)
        if not data:
            break
        df = pd.DataFrame(data)
       # df = pd.read_json(response.text)
        dfAll = pd.concat([df,dfAll])
        all_data.extend(data)
        page_num += 1
        #time.sleep(1)  # Respect rate limits (e.g., 10-30 calls per minute)
    dfAll.to_pickle("markets.pkl")
    print(f"Total coins fetched: {len(all_data)}")
    return

def fetch_all_coins():

    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    headers = {
        "accept": "application/json",
        #"x-cg-demo-api-key": "CG-ULEXj9kgbnAK2kGvieVgsDBL"
    }
    response = requests.get(url, headers=headers)
    df_coins = pd.read_json(response.text)
    df_coins.to_pickle("coins.pkl")
    return

def fetch_coins_simple(coinIds):
    url = "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=full"
    headers = {
        "accept": "application/json",
        #"x-cg-demo-api-key": "CG-ULEXj9kgbnAK2kGvieVgsDBL"
    }
    url += f"&ids={coinIds}"
   
    response = requests.get(url, headers=headers)
    print(response.text)
    df_coins = pd.read_json(response.text)
    df_coins.to_pickle("coins_simple.pkl")
    return

def create_market_table(df):
    columns = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']
    # Create a ColumnDataSource from the Pandas DataFrame
    source = ColumnDataSource(df)
    # Define table columns
    columns = [TableColumn(field=col, title=col) for col in columns]

    # Create DataTable widget
    data_table = DataTable(source=source, columns=columns, width=400, height=280, sizing_mode='stretch_both')
    return data_table

def create_simple_table(df):
    columns = ['usd', 'usd_market_cap', 'usd_24h_vol', 'usd_24h_change', 'last_updated_at']
    # Create a ColumnDataSource from the Pandas DataFrame
    source = ColumnDataSource(df)
    # Define table columns
    columns = [TableColumn(field=col, title=col) for col in columns]

    # Create DataTable widget
    data_table = DataTable(source=source, columns=columns, width=400, height=280, sizing_mode='stretch_both')
    return data_table

#fetch_all_markets()
#fetch_all_coins()

df = pd.read_pickle("markets.pkl")
df_coins = pd.read_pickle("coins.pkl")

df = df_coins.merge(df, on = 'id', how = 'left')
df = df[df['platforms'].apply(lambda x: "solana" in x)]
df = df[df['market_cap'].apply(lambda x: x > 0)]
df = df[df['total_volume'].apply(lambda x: x > 10000)]
df = df[df['price_change_percentage_24h'].apply(lambda x: x > 10)]

coinIds = ''
coinTotal = 0
for index, row in df.iterrows():
    if (coinTotal > 0):
        coinIds += "%2C"
    coinIds += f"{row['id']}"
    coinTotal+=1

print (f"Total coins: {coinTotal}")
#fetch_coins_simple(coinIds)
df_coins_simple = pd.read_pickle("coins_simple.pkl").transpose()
print (df_coins_simple)
df_coins_simple2 = pd.DataFrame()
for index, row in df.df_coins_simple():
    df_coins_simple2 += row['id']


data_table = create_simple_table(df_coins_simple2)
show(data_table)
#curdoc().add_root(data_table)