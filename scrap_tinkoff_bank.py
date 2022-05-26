# source page https://www.tinkoff.ru/about/exchange/

import requests
import json


def get_prices_and_spread_from_tinkoffbank(timeout=15):
    url = 'https://api.tinkoff.ru/v1/currency_rates?from=USD&to=RUB'

    headers = {
        'authority': 'api.tinkoff.ru',
        'method': 'GET',
        'path': '/v1/currency_rates?from=USD&to=RUB',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.tinkoff.ru',
        'referer': 'https://www.tinkoff.ru/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.42'
    }

    res = requests.get(url=url, headers=headers, timeout=timeout)
    data_dict = json.loads(res.text)

    price_buy_tinkoff = float(data_dict.get('payload').get('rates')[2].get('sell'))
    price_sell_tinkoff = float(data_dict.get('payload').get('rates')[2].get('buy'))

    spread_tinkoff = round(price_buy_tinkoff - price_sell_tinkoff, 2)

    return price_buy_tinkoff, price_sell_tinkoff, spread_tinkoff


def main():
    price_buy_tinkoff, price_sell_tinkoff, spread_tinkoff = get_prices_and_spread_from_tinkoffbank()
    print(f'Tinkoff-bank\n'
          f'покупка/продажа \u0394 разница\n'
          f'{price_buy_tinkoff:.2f}/{price_sell_tinkoff:.2f} \u0394{spread_tinkoff:.2f}')


if __name__ == '__main__':
    main()
