
class Stock:
    def __init__(self, gbls, sid):
        self._sid = sid
        self._gbls = gbls

    def id(self):
        return self._sid

    # This info come from recent prices or history prices
    def price(self, date = None):
        return self._gbls.price(self._sid, date)

    def name(self):
        mp = self._gbls.stockidnamemapping()
        return mp.getname(self._sid)

    # Below info come from history prices
    def historyprice(self, date):
        return self._gbls.historyprice(self._sid, date)

    def historymarketvalue(self, date):
        return self._gbls.historymarketvalue(self._sid, date)

    def historypricesrange(self):
        return self._gbls.historypricesrange(self._sid)

    # return price, and share change on this date
    def historypricesshare(self, date):
        return self._gbls.historypricesshare(self._sid, date)

    def gethpssimplelist(self):
        return self._gbls.gethpssimplelist(self._sid)



if __name__ == "__main__":
    from moneyseav3.globals import Globals

    idx = "0000001" #"300230"
    gbls = Globals.get_instance()
    s = Stock(gbls, idx)
    print s.id()
    print s.name()
    print s.price((2018, 12, 27))
