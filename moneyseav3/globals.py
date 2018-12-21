from moneyseav3.resources.stockidnamemapping import StockIdNameMapping
from moneyseav3.resources.stock import Stock
from moneyseav3.resources.prices import Prices


class Globals:
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self._stockidnamemapping = StockIdNameMapping()
        sim = self._stockidnamemapping.getmap()

        self._stocks = {}
        for sid in sim:
            self._stocks[sid] = Stock(self, sid)

        self._prices = Prices()


    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Globals()
        return cls.INSTANCE


    # return dict of {stockid:Stock}. Financial data may not be ready.
    def stocks(self):
        return self._stocks


    # for Stock class usage
    def price(self, sid, date = None):
        return self._prices.price(sid, date)


if __name__ == "__main__":
    pass
