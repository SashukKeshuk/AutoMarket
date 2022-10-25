from bitcoin import *
from db import get_wallet, close_able, open_able
import time
import requests

def init():
    wallets = get_wallet()
    wallet = {
        'addr' : wallets[0]['addr'],
        'bal' : wallets[0]['balance']
    }
    close_able(wallet['addr'])
    return wallet

def check(wallet, balance):
    url = "https://bitcoin-api.p.rapidapi.com/balancesByAddress"
    payload = {"addresses": [wallet]}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "YOUR_KEY_HERE",
        "X-RapidAPI-Host": "bitcoin-api.p.rapidapi.com"
    }
    start_time = time.time()
    while True:
        if (start_time-time.time()>3600):
            open_able(wallet)
            return 0
        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.text
        bal = float(data[0]['data']['btc'])
        if (bal > balance):
            open_able(wallet)
            return (bal-balance)
        time.sleep(10)
