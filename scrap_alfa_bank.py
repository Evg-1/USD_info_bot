# source page https://alfabank.ru/currency/

import requests
import datetime
import json
from settings import PROXY_AUTH


def get_prices_and_spread_from_alfabank(timeout=15):
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    url = f'https://alfabank.ru/api/v1/scrooge/currencies/alfa-rates?currencyCode.in=USD,EUR,CHF,GBP&rateType.eq=makeCash&lastActualForDate.eq=true&clientType.eq=standardCC&date.lte={now}%2B03:00'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'site_city=moscow; platformId=alfasite; _gcl_au=1.1.719283659.1647777234; ab_test_ao=ok; _ym_uid=1647777234148977412; _ym_d=1647777234; prodID=Other; gtm-session-start=1647777233026; _sp_ses.3c2b=*; _ym_visorc=b; _ym_isad=1; tmr_lvid=de0c3a9360b352d8f63558f05465cd12; tmr_lvidTS=1647777234472; _clck=9hw6ie|1|ezx|0; _gid=GA1.2.428222727.1647777238; stopTimer30secOnsite=1; alfa_ia_param_ya_cid=1647777234148977412; staduid=https%3A%2F%2Falfabank.ru%2Fcurrency%2F; _dc_gtm_UA-1247553-1=1; _ga=GA1.1.1125761959.1647777234; tmr_detect=1%7C1647779085839; _clsk=wmsfc8|1647779086541|10|1|l.clarity.ms/collect; _sp_id.3c2b=88ca34d2-4cc2-4582-b17c-a87f05e7e2d9.1647777234.1.1647779116.1647777234.5490851e-de74-4f43-9007-3d313c3547a1; tmr_reqNum=96; _ga_Z8EEZ8QGKE=GS1.1.1647777234.1.1.1647779125.0',
        'Host': 'alfabank.ru',
        'Referer': 'https://alfabank.ru/currency/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
    }

    proxies = {
        'https': PROXY_AUTH
    }

    # response = requests.get(url=url, headers=headers, timeout=10)
    response = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout)

    data_dict = json.loads(response.text)

    price_buy_alfa = float(data_dict.get('data')[3].get('rateByClientType')[0].get('ratesByType')[0]
                           .get('lastActualRate').get('sell').get('originalValue'))
    price_sell_alfa = float(data_dict.get('data')[3].get('rateByClientType')[0].get('ratesByType')[0]
                            .get('lastActualRate').get('buy').get('originalValue'))

    spread_alfa = price_buy_alfa - price_sell_alfa
    spread_alfa = round(spread_alfa, 2)

    return price_buy_alfa, price_sell_alfa, spread_alfa


def main():
    price_buy_alfa, price_sell_alfa, spread_alfa = get_prices_and_spread_from_alfabank()
    print(f'Alfa-bank:\n'
          f'покупка/продажа \u0394 разница\n'
          f'{price_buy_alfa:.2f}/{price_sell_alfa:.2f} \u0394{spread_alfa:.2f}')


if __name__ == '__main__':
    main()
