from moneyseav3.globals import Globals
from moneyseav3.resources.stock import Stock
import datetime, time

class GroupPrice:
    def __init__(self, ss, start, end):
        share = {}
        for idx in ss:
            S = Stock(Globals.get_instance(), idx)
            ps = S.historypricesshare(start)
            #use 20000 to buy it in 100 shares
            if ps == None:
                share[idx] = (0, 0)
            else:
                share[idx] = (int(20000 / ps[0]), ps[0])
        self._db = {}
        self._db["%04d-%02d-%02d"%start] = share

        self.setup(start, end)
        pass

    def setup(self, start, end):
        try:
            startdate = datetime.date(start[0], start[1], start[2])
        except:
            return

        tmptime = time.mktime(startdate.timetuple())
        endstr = "%04d-%02d-%02d"%(end[0], end[1], end[2])
        init = prev = self._db["%04d-%02d-%02d"%start]
        while True:
            tmptime += (3600*24)
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break
            share = {}
            for idx in init:
                S = Stock(Globals.get_instance(), idx)
                ps = S.historypricesshare((dt.year, dt.month, dt.day))
                if ps == None:
                    share[idx] = (prev[idx][0], prev[idx][1])
                else:
                    if ps[1] == 1:
                        share[idx] = (prev[idx][0], ps[0])
                    elif ps[1] == 0:
                        share[idx] = (prev[idx][0], ps[0])
                    else:
                        share[idx] = (prev[idx][0]*ps[1], ps[0])
                prev = share
            self._db[str(dt)] = share 
        pass

    def price(self, date):
        dstr = "%04d-%02d-%02d"%(date[0], date[1], date[2])
        mm = self._db[dstr]
        p = 0
        for idx in mm:
            p += (mm[idx][0] * mm[idx][1])
        return p

if __name__ == "__main__":
    gp = GroupPrice(("300230", "300231"), (2018, 11, 1), (2018, 11, 28))
    print gp.price((2018, 11, 2))
    pass










