
import datetime, time

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

    # return a valid price near date, [date, date + range]
    def validhistorypricesshare(self, date, rng):
        dt = datetime.date(date[0], date[1], date[2])
        start = time.mktime(dt.timetuple())
        for i in range(0, rng):
            tmptime = start + i * (3600*24)
            ndt = datetime.date.fromtimestamp(tmptime)
            hps = self._gbls.historypricesshare(self._sid, (ndt.year, ndt.month, ndt.day))
            if hps == None:
                continue
            return hps
        return None

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
