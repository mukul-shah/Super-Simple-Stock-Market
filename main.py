from stock_market import StockMarket
from stock_data_config import stock_data, indicators
if __name__ == '__main__':
    menu_main = "Enter the Option you want:\n" \
                "1. Dividend yield\n" \
                "2. P/E Ratio\n" \
                "3. Book Trade\n" \
                "4. Volume Weighted Stock Price\n" \
                "5. GBCE All Share Index\n" \
                "6. Exit\n"

    menu_stocks = ["Choose a stock:"] + [str(index+1)+'. '+val for index, val in enumerate(stock_data.keys())]

    menu_buy_sell = ["Please select:"] + [str(index+1)+'. '+val for index, val in enumerate(indicators)]

    menu_option_list = list(range(1, 7))
    stockMarketObj = StockMarket()
    while True:
        try:
            option = int(input(menu_main))
            if option not in menu_option_list:
                print("Invalid Option, Select from below options only: \n")

            elif option == 6:
                break

            elif option == 1:
                symbol = int(input('\n'.join(map(str, menu_stocks))))
                price = input("Enter the stock price:\n")
                dividend_yield = stockMarketObj.calculate_dividend_yield(symbol, price)
                print("Dividend Yield : %s\n" % dividend_yield)

            elif option == 2:
                symbol = int(input('\n'.join(map(str, menu_stocks))))
                price = input("Enter the stock price: \n")
                pe_ratio = stockMarketObj.calculate_pe_ratio(symbol, price)
                print("P/E Ratio : %s\n" % pe_ratio)

            elif option == 3:
                symbol = int(input('\n'.join(map(str, menu_stocks))))
                quantity = input("Quantity of shares: \n")
                indicator = int(input('\n'.join(map(str, menu_buy_sell))))
                traded_price = input("Enter Trade Price: \n")
                print(stockMarketObj.record_trade(symbol, quantity, indicator, traded_price))

            elif option == 4:
                symbol = int(input('\n'.join(map(str, menu_stocks))))
                print(stockMarketObj.volume_weighted_stock_price(symbol))

            elif option == 5:
                print(stockMarketObj.all_share_index())

        except Exception:
            print("Invalid option")
            pass
