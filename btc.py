import requests as req
import json


''' Gets Bitcoin Price Using Coinbase API '''


def get_btc_price():

    r = req.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
    js = r.content
    dict = json.loads(js)['data']
    price = float(dict['amount'])
    return price




