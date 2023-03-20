from binance.spot import Spot


def get_price(pair):
    bitcoin = Spot().ticker_price(pair)
    price = bitcoin['price']
    price = price [:-6]+" $"
    return price

def get_price_wd(pair):
    bitcoin = Spot().ticker_price(pair)
    price = bitcoin['price']
    price = float(price [:-6])
    return price

