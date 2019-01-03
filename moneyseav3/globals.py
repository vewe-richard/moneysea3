from moneyseav3.resources.stockidnamemapping import StockIdNameMapping
from moneyseav3.resources.stock import Stock
from moneyseav3.resources.prices import Prices
from moneyseav3.resources.oneholdedrecord import OneHoldedRecord
from moneyseav3.resources.ff10jqka import FF10jqka


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
        self._ff10jqka = None


    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Globals()
        return cls.INSTANCE


    # return dict of {stockid:Stock}. Financial data may not be ready.
    def stocks(self):
        return self._stocks

    def getstock(self, stockid):
        return self._stocks[stockid]

    def oneholdedrecord(self, recordpath):
        return OneHoldedRecord(recordpath)


    # for Stock class usage
    def price(self, sid, date = None):
        return self._prices.price(sid, date)

    def historyprice(self, sid, date):
        return self._prices.historyprice(sid, date)
    def historymarketvalue(self, sid, date):
        return self._prices.historymarketvalue(sid, date)
    def historypricesrange(self, sid):
        return self._prices.historyrange(sid)
    def historypricesshare(self, sid, date):
        return self._prices.historypricesshare(sid, date)
    def gethpssimplelist(self, sid):
        return self._prices.gethpssimplelist(sid)

    def stockidnamemapping(self):
        return self._stockidnamemapping

    def getff10jqka(self):
        if self._ff10jqka == None:
            self._ff10jqka = FF10jqka()
        return self._ff10jqka

if __name__ == "__main__":
    gbls = Globals.get_instance()
    print gbls.price("0000001", (2018,12,27))
    pass






