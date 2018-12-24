
class Stock:
    def __init__(self, gbls, sid):
        self._sid = sid
        self._gbls = gbls

    def id(self):
        return self._sid

    # This info come from recent prices or history prices
    def price(self, date = None):
        return self._gbls.price(self._sid, date)

    # Below info come from history prices
    def historyprice(self, date):
        return self._gbls.historyprice(self._sid, date)

    def historymarketvalue(self, date):
        return self._gbls.historymarketvalue(self._sid, date)

    def historypricesrange(self):
        return self._gbls.historypricesrange(self._sid)


