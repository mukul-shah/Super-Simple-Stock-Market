from datetime import datetime, timedelta
from stock_data_config import stock_data, indicators, timestamp_interval


class StockMarket:
    def __init__(self):
        self.stock_symbol = {index+1: val for index, val in enumerate(stock_data.keys())}
        self.indicator_mapping = {index+1: val for index, val in enumerate(indicators)}
        self.trade_record = []

    def calculate_dividend_yield(self, symbol, price):
        """ Calculate dividend yield for given stock and price. """
        try:
            stock_symbol = self.stock_symbol[symbol]
        except KeyError:
            return "Enter Valid Stock Symbol"
        try:
            if float(price) <= 0.0:
                return "Enter valid price"
        except ValueError:
            return "Enter valid price"

        stock = stock_data.get(stock_symbol, None)
        dividend_yield = 0
        price = float(price)
        try:
            if stock['type'] == "Common":
                dividend_yield = float(stock.get('last_dividend', 0)) / price
            elif stock['type'] == "Preferred":
                fixed_dividend = float(stock.get('fixed_dividend', 0)) / 100
                par_value = float(stock.get('par_value', 0))
                dividend_yield = fixed_dividend * par_value / price
        except ZeroDivisionError:
            pass
        return dividend_yield

    def calculate_pe_ratio(self, symbol, price):
        """ Calculate PE Ratio for given stock and price. """
        pe_ratio = 0
        try:
            dividend_yield = self.calculate_dividend_yield(symbol, price)
            pe_ratio = float(price) / float(dividend_yield)
        except ZeroDivisionError:
            pass
        return pe_ratio

    def record_trade(self, symbol, quantity, indicator, traded_price):
        """ Record a new trade in the stock. """

        try:
            stock_symbol = self.stock_symbol[symbol]
        except KeyError:
            return "Enter only stock symbol as in {0}".format(stock_data.keys())
        try:
            indicator = self.indicator_mapping[indicator]
        except KeyError:
            return "Enter indicator as in {0}".format(indicators)

        try:
            self.create_trade_record_data(stock_symbol, int(quantity),
                                          indicator, float(traded_price), datetime.now())
            return "Trade recorded successfully."
        except Exception:
            return "Trade recorded Failed."

    def volume_weighted_stock_price(self, stock_symbol):
        """ Calculate stock price for given stock from particular interval trades. """

        time_interval = datetime.now() - timedelta(minutes=timestamp_interval)
        stock_quantity_sum = 0
        sum_stock_trade_price = 0

        if len(self.trade_record) > 0:
            for record in self.trade_record:
                if record['stock_symbol'] == self.stock_symbol[stock_symbol] and record['trade_timestamp'] >= time_interval:
                    stock_quantity_sum += record['quantity']
                    sum_stock_trade_price += (record['quantity'] * record['traded_price'])
            if sum_stock_trade_price and stock_quantity_sum:
                vol_weight_stock_price = float(sum_stock_trade_price / stock_quantity_sum)
                return vol_weight_stock_price
            else:
                return "No trade record for the stock {0} in the past {1} minutes".format(stock_symbol, timestamp_interval)
        else:
            return "No trade records"

    def all_share_index(self):
        """ Calculate GBCE All Share Index by using geometric mean of prices for all stocks. """
        stock_quantity_sum = 0
        sum_stock_trade_price = 0

        if len(self.trade_record) > 0:
            for record in self.trade_record:
                stock_quantity_sum += record['quantity']
                sum_stock_trade_price += (record['quantity'] * record['traded_price'])
            if sum_stock_trade_price and stock_quantity_sum:
                all_share_index = sum_stock_trade_price ** (1 / stock_quantity_sum)
                return float(all_share_index)
        return "Trade Record is empty"

    def create_trade_record_data(self, stock_symbol, quantity, indicator, traded_price, timestamp):
        record = {
            "stock_symbol": stock_symbol,
            "quantity": quantity,
            "indicator": indicator,
            "traded_price": traded_price,
            "trade_timestamp": timestamp
        }
        self.trade_record.append(record)

