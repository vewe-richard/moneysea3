
class Stock:
    def __init__(self, gbls, sid):
        self._sid = sid
        self._gbls = gbls

    def id(self):
        return self._sid

    def price(self, date = None):
        return self._gbls.price(self._sid, date)


