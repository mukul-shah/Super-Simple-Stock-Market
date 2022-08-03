import unittest

from stock_market import StockMarket


class StockMarketTest(unittest.TestCase):
    def setUp(self):
        self.stock_market = StockMarket()
        self.symbol = 3
        self.quantity = 22
        self.indicator = 1
        self.traded_price = 90
        self.price = 100

    def test_record_trade(self):
        self.stock_market.record_trade(self.symbol, self.quantity, self.indicator, self.traded_price)
        self.assertTrue(len(self.stock_market.trade_record) > 0)

    def test_volume_weighted_stock_price(self):
        self.stock_market.record_trade(self.symbol, self.quantity, self.indicator, self.traded_price)
        vol_weighted_price = self.stock_market.volume_weighted_stock_price(self.symbol)
        self.assertEqual(vol_weighted_price, self.traded_price)

    def test_volume_weighted_stock_price_no_trade_record(self):
        vol_weighted_price = self.stock_market.volume_weighted_stock_price(self.symbol)
        self.assertEqual(vol_weighted_price, 'No trade records')

    def test_calculate_dividend_yield(self):
        dividend_yield = self.stock_market.calculate_dividend_yield(self.symbol, self.price)
        self.assertEqual(dividend_yield, 0.23)

    def test_calculate_pe_ratio(self):
        pe_ratio = self.stock_market.calculate_pe_ratio(self.symbol, self.price)
        self.assertEqual(round(pe_ratio, 1), 434.8)

    def test_all_share_index(self):
        self.stock_market.record_trade(self.symbol, self.quantity, self.indicator, self.traded_price)
        self.assertTrue(self.stock_market.all_share_index() > 0)

    def test_all_share_index_no_trade_record(self):
        self.assertEqual(self.stock_market.all_share_index(), "Trade Record is empty")


if __name__ == "__main__":
    unittest.main()
