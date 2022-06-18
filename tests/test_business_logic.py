import os

os.chdir(os.path.join(os.path.dirname(__file__),
                      os.path.pardir))  # поднимаемся на 1 директорию выше, чтобы дотянуться до .env

import unittest
from business_logic import Usd


class UsdTest(unittest.TestCase):

    def setUp(self):
        self.usd = Usd()

    def test_get_prices_and_spread_from_binance_p2p(self):
        self.usd.get_prices_and_spread_from_binance_p2p()
        self.assertAlmostEqual(self.usd.price_buy_binance, 100, delta=90)
        self.assertAlmostEqual(self.usd.price_sell_binance, 100, delta=90)
        self.assertAlmostEqual(self.usd.spread_binance, 30, delta=40)

    def test_get_prices_and_spread_from_alfabank(self):
        self.usd.get_prices_and_spread_from_alfabank()
        self.assertAlmostEqual(self.usd.price_buy_alfa, 100, delta=90)
        self.assertAlmostEqual(self.usd.price_sell_alfa, 100, delta=90)
        self.assertAlmostEqual(self.usd.spread_alfa, 30, delta=40)

    def test_get_prices_and_spread_from_tinkoffbank(self):
        self.usd.get_prices_and_spread_from_tinkoffbank()
        self.assertAlmostEqual(self.usd.price_buy_tinkoff, 100, delta=90)
        self.assertAlmostEqual(self.usd.price_sell_tinkoff, 100, delta=90)
        self.assertAlmostEqual(self.usd.spread_tinkoff, 30, delta=40)

    def test_get_formatted_msg_from_binance_p2p(self):
        self.usd.get_formatted_msg_from_binance_p2p()
        self.assertRegex(self.usd.binance_p2p_f_msg, r'\d+\.\d\d/\d+\.\d\d Δ-?\d+\.\d\d')

    def test_get_formatted_msg_from_alfabank(self):
        self.usd.get_formatted_msg_from_alfabank()
        self.assertRegex(self.usd.alfabank_p2p_f_msg, r'\d+\.\d\d/\d+\.\d\d Δ-?\d+\.\d\d')

    def test_get_formatted_msg_from_tinkoffbank(self):
        self.usd.get_formatted_msg_from_tinkoffbank()
        self.assertRegex(self.usd.tinkoffbank_p2p_f_msg, r'\d+\.\d\d/\d+\.\d\d Δ-?\d+\.\d\d')
