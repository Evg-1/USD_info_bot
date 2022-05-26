# pip install beautifulsoup4 requests lxml
# source page https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=RUB выбрать способ оплаты 'Тинькофф'

import requests
import json


def get_prices_and_spread_from_binance_p2p(timeout=15):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        'authority': 'p2p.binance.com',
        'method': 'POST',
        'path': '/bapi/c2c/v2/friendly/c2c/adv/search',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'bnc-uuid': 'ada2c8e8-d768-4f06-b5af-3fc2a193b611',
        'c2ctype': 'c2c_merchant',
        'clienttype': 'web',
        'content-length': '101',
        'content-type': 'application/json',
        'cookie': 'cid=ft6j85yg; _ga=GA1.2.2072649705.1618569896; bnc-uuid=ada2c8e8-d768-4f06-b5af-3fc2a193b611; source=organic; campaign=www.google.com; userPreferredCurrency=USD_USD; fiat-prefer-currency=USD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22178da48a5436a9-0c986672bf10b3-4d5a4451-2073600-178da48a544ab2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22178da48a5436a9-0c986672bf10b3-4d5a4451-2073600-178da48a544ab2%22%7D; lang=en; _gcl_au=1.1.12394391.1647628396; _gid=GA1.2.2135133776.1647628396; BNC_FV_KEY_EXPIRE=1647714796404; BNC_FV_KEY=3184b867cad1aa07a65de49a502f1541c4258785; showBlockMarket=false; _gat_UA-162512367-1=1; sys_mob=no; _uetsid=e066eb80a6e911ec977fc35c13ac11fa; _uetvid=e0674b10a6e911ec94b16dec6b010795; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Mar+19+2022+11%3A19%3A04+GMT%2B0300+(Moscow+Standard+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=59137b16-c2c6-432b-8110-a43cb8658f04&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false; common_fiat=RUB; videoViewed=yes',
        'csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
        'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA0MCIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoiZW4tVVMiLCJ0aW1lem9uZSI6IkdNVCszIiwidGltZXpvbmVPZmZzZXQiOi0xODAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTguMC40NzU4LjEwOSBTYWZhcmkvNTM3LjM2IE9QUi84NC4wLjQzMTYuMzEiLCJsaXN0X3BsdWdpbiI6IlBERiBWaWV3ZXIsQ2hyb21lIFBERiBWaWV3ZXIsQ2hyb21pdW0gUERGIFZpZXdlcixNaWNyb3NvZnQgRWRnZSBQREYgVmlld2VyLFdlYktpdCBidWlsdC1pbiBQREYiLCJjYW52YXNfY29kZSI6ImE0MGRkYTMyIiwid2ViZ2xfdmVuZG9yIjoiR29vZ2xlIEluYy4gKE5WSURJQSkiLCJ3ZWJnbF9yZW5kZXJlciI6IkFOR0xFIChOVklESUEsIE5WSURJQSBHZUZvcmNlIFJUWCAyMDgwIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEtMzAuMC4xNS4xMTc5KSIsImF1ZGlvIjoiMTI0LjA0MzQ3NTI3NTE2MDc0IiwicGxhdGZvcm0iOiJXaW4zMiIsIndlYl90aW1lem9uZSI6IkV1cm9wZS9Nb3Njb3ciLCJkZXZpY2VfbmFtZSI6Ik9wZXJhIFY4NC4wLjQzMTYuMzEgKFdpbmRvd3MpIiwiZmluZ2VycHJpbnQiOiI1OTdjNWExMGVlY2FmNDU2OTc1YTgxYzAwMDczMGEwZCIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IiJ9',
        'fvideo-id': '3184b867cad1aa07a65de49a502f1541c4258785',
        'lang': 'ru',
        'origin': 'https://p2p.binance.com',
        'referer': 'https://p2p.binance.com/ru?fiat=RUB&payment=ALL',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Opera";v="84"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.31',
        'x-trace-id': '69909413-e83c-44e0-a38d-cf2e7fef4a1f',
        'x-ui-request-trace': '69909413-e83c-44e0-a38d-cf2e7fef4a1f'
    }

    request_payload_buy = {"page": 1, "rows": 10, "payTypes": ["Tinkoff"], "asset": "USDT", "tradeType": "BUY",
                           "fiat": "RUB", "publisherType": None}
    response = requests.post(url=url, headers=headers, json=request_payload_buy, timeout=timeout)
    # print(f'Status_code_is {response.status_code}')
    data_dict = json.loads(response.text)
    price_buy_binance = float(data_dict.get('data')[0].get('adv').get('price'))

    request_payload_sell = {"page": 1, "rows": 10, "payTypes": ["Tinkoff"], "asset": "USDT", "tradeType": "SELL",
                            "fiat": "RUB", "publisherType": None}
    response = requests.post(url=url, headers=headers, json=request_payload_sell, timeout=timeout)
    # print(f'Status_code_is {response.status_code}')
    data_dict = json.loads(response.text)
    price_sell_binance = float(data_dict.get('data')[0].get('adv').get('price'))

    spread_binance = round(price_buy_binance - price_sell_binance, 2)

    return price_buy_binance, price_sell_binance, spread_binance


def main():
    price_buy_binance, price_sell_binance, spread_binance = get_prices_and_spread_from_binance_p2p()
    print(f'Binance p2p через Tinkoff:\n'
          f'покупка/продажа \u0394 разница\n'
          f'{price_buy_binance:.2f}/{price_sell_binance:.2f} \u0394{spread_binance:.2f}')


if __name__ == '__main__':
    main()
