from datetime import datetime, timedelta
import json
from threading import Thread

import requests
from requests.adapters import HTTPAdapter, Retry

from utils.cfg_logging import log
from settings import USE_PROXY

if USE_PROXY is True:
    from settings import PROXIES

    log.info('proxy используется')
else:
    PROXIES = None


class Usd:
    def __init__(self):
        self.price_buy_binance = None
        self.price_sell_binance = None
        self.spread_binance = None
        self.price_buy_alfa = None
        self.price_sell_alfa = None
        self.spread_alfa = None
        self.price_buy_tinkoff = None
        self.price_sell_tinkoff = None
        self.spread_tinkoff = None
        self.bot_prices_info_reply = None
        self.binance_f_msg = None
        self.alfabank_f_msg = None
        self.tinkoffbank_f_msg = None

    @staticmethod
    def get_data(url: str, headers: dict, payload: dict = None, timeout: int = 5, proxies: dict = PROXIES):
        if payload is None:  # используем метод GET
            session = requests.Session()
            retry_strategy = Retry(total=3, backoff_factor=1)
            session.mount('https://', HTTPAdapter(max_retries=retry_strategy))
            return session.get(url=url, headers=headers, timeout=timeout, proxies=proxies)
        else:  # используем метод POST
            session = requests.Session()
            retry_strategy = Retry(total=3, backoff_factor=1)
            session.mount('https://', HTTPAdapter(max_retries=retry_strategy))
            return session.post(url=url, headers=headers, timeout=timeout, proxies=proxies, json=payload)

    @staticmethod
    def calc_spread(price_buy: (int, float), price_sell: (int, float)) -> float:
        """
        Вычисляем spread - разницу между ценой_покупки и ценой_продажи
        """
        return float(round(price_buy - price_sell, 2))

    def get_prices_and_spread_from_binance_p2p(self):
        """
        Получить цену покупки, цену продажи и разницу между ними с binance_p2p
        для ручного просмотра зайти на
        https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=RUB
        и выбрать способ оплаты 'Тинькофф'
        """

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

        payload_buy = {"page": 1, "rows": 10, "payTypes": ["TinkoffNew"], "asset": "USDT", "tradeType": "BUY",
                       "fiat": "RUB", "publisherType": None}
        response_buy = self.get_data(url=url, headers=headers, payload=payload_buy)
        response_buy_dict = json.loads(response_buy.text)
        self.price_buy_binance = float(response_buy_dict.get('data')[0].get('adv').get('price'))

        payload_sell = {"page": 1, "rows": 10, "payTypes": ["TinkoffNew"], "asset": "USDT", "tradeType": "SELL",
                        "fiat": "RUB", "publisherType": None}
        response_sell = self.get_data(url=url, headers=headers, payload=payload_sell)
        response_sell_dict = json.loads(response_sell.text)
        self.price_sell_binance = float(response_sell_dict.get('data')[0].get('adv').get('price'))

        self.spread_binance = self.calc_spread(self.price_buy_binance, self.price_sell_binance)

    def get_prices_and_spread_from_alfabank(self):
        """
        Получить цену покупки, цену продажи и разницу между ними из Альфа банка
        для ручного просмотра зайти на https://alfabank.ru/currency/
        """
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        url = f'https://alfabank.ru/api/v1/scrooge/currencies/alfa-rates?currencyCode.in=USD,EUR,CHF,GBP&rateType.eq=makeCash&lastActualForDate.eq=true&clientType.eq=standardCC&date.lte={now}%2B03:00'

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        response = self.get_data(url=url, headers=headers)

        response_dict = json.loads(response.text)

        self.price_buy_alfa = float(response_dict.get('data')[3].get('rateByClientType')[0].get('ratesByType')[0]
                                    .get('lastActualRate').get('sell').get('originalValue'))
        self.price_sell_alfa = float(response_dict.get('data')[3].get('rateByClientType')[0].get('ratesByType')[0]
                                     .get('lastActualRate').get('buy').get('originalValue'))

        self.spread_alfa = self.calc_spread(self.price_buy_alfa, self.price_sell_alfa)

    def get_prices_and_spread_from_tinkoffbank(self):
        """
        Получить цену покупки, цену продажи и разницу между ними из Тинькофф банка
        для ручного просмотра зайти на https://www.tinkoff.ru/about/exchange/
        """

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

        response = self.get_data(url=url, headers=headers)
        response_dict = json.loads(response.text)

        self.price_buy_tinkoff = float(response_dict.get('payload').get('rates')[2].get('sell'))
        self.price_sell_tinkoff = float(response_dict.get('payload').get('rates')[2].get('buy'))

        self.spread_tinkoff = self.calc_spread(self.price_buy_tinkoff, self.price_sell_tinkoff)

    def get_formatted_msg_from_binance_p2p(self):
        try:
            self.get_prices_and_spread_from_binance_p2p()
        except Exception as exc:
            log.exception(exc)
            self.binance_f_msg = 'не удалось получить данные 😭'
        else:
            self.binance_f_msg = f'{self.price_buy_binance:.2f}/{self.price_sell_binance:.2f} Δ{self.spread_binance:.2f}'

    def get_formatted_msg_from_alfabank(self):
        try:
            self.get_prices_and_spread_from_alfabank()
        except Exception as exc:
            log.exception(exc)
            self.alfabank_f_msg = 'не удалось получить данные 😭'
        else:
            self.alfabank_f_msg = f'{self.price_buy_alfa:.2f}/{self.price_sell_alfa:.2f} Δ{self.spread_alfa:.2f}'

    def get_formatted_msg_from_tinkoffbank(self):
        try:
            self.get_prices_and_spread_from_tinkoffbank()
        except Exception as exc:
            log.exception(exc)
            self.tinkoffbank_f_msg = 'не удалось получить данные 😭'
        else:
            self.tinkoffbank_f_msg = f'{self.price_buy_tinkoff:.2f}/{self.price_sell_tinkoff:.2f} Δ{self.spread_tinkoff:.2f}'

    def get_bot_prices_info_reply(self):
        funcs = [self.get_formatted_msg_from_binance_p2p,
                 self.get_formatted_msg_from_alfabank,
                 self.get_formatted_msg_from_tinkoffbank]

        threads = [Thread(target=func) for func in funcs]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        self.bot_prices_info_reply = str(f'Binance p2p:\n'
                                         f'<code>{self.binance_f_msg}</code>\n'
                                         f'Alfa-bank:\n'
                                         f'<code>{self.alfabank_f_msg}</code>\n'
                                         f'Tinkoff-bank\n'
                                         f'<code>{self.tinkoffbank_f_msg}</code>')


if __name__ == '__main__':
    usd = Usd()
    usd.get_bot_prices_info_reply()
    print(usd.bot_prices_info_reply.replace('<code>', '').replace('</code>', ''))
