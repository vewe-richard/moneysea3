
# coding=utf-8
from moneyseav3.globals import Globals
from moneyseav3.config import Config
import datetime, time
import json

class HistoryPricesShare:
    def run(self):
        gbls = Globals.get_instance()
        count = 0
        self._stats = {"total":0, "nodata":0, "none": 0, "zero":0, "same": 0, "minidelta":0, "sendingshare":0, "addshare":0, "left": 0,}
        for s in gbls.stocks():
            S = gbls.stocks()[s]
            self.verifytotalshares(S)
            count += 1
            if count > 0:
                pass
#                break

        total = self._stats["total"]
        print "nodata: number of stocks without price data \t", self._stats["nodata"]
        print ""

        self.printstat("none", "price or marketvalue are None, 比如节假日休市没有数据\t", total)
        self.printstat("zero", "price or marketvalue are zero, 比如停牌\t\t", total)
        self.printstat("same", "totalshare is not changed\t\t\t", total)
        self.printstat("minidelta", "totalshare 变更较小\t\t\t", total)
        self.printstat("sendingshare", "送股行为\t\t\t\t", total)
        self.printstat("addshare", "增资扩股\t\t\t\t", total)

        self.printstat("left", "left cases\t\t\t", total)

        print "Left: ", self._stats["left"]

    def printstat(self, key, descriptor, total):
        print key, ":", descriptor, 100.0*self._stats[key]/total, "%"

    def verifytotalshares(self, S):
        rng = S.historypricesrange()
        startstr = rng[0]
#        if startstr < "2010-01-01":
#            startstr = "2010-01-01"

        endstr = rng[1]

        items = startstr.split("-")

        try:
            startdate = datetime.date(int(items[0]), int(items[1]), int(items[2]))
        except:
            #without correct history prices
            self._stats["nodata"] += 1
            return

        tmptime = time.mktime(startdate.timetuple())

        p1 = None
        mv1 = None
        pricesshare = {}
        while True:
            self._stats["total"] += 1
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break
            p = S.historyprice(self.date(dt))
            mv = S.historymarketvalue(self.date(dt))
            if p == None or mv == None:
                tmptime += (3600*24)
                self._stats["none"] += 1
                continue

            if p < 0.01 or mv < 0.01:
                tmptime += (3600*24)
                self._stats["zero"] += 1
                continue
            
            if p1 == None:
                pricesshare[str(dt)] = (p, 1, int(mv/10000))
            else:
                pricesshare[str(dt)] = self.caculate(S, dt, p1, mv1, p, mv)
            p1 = p
            mv1 = mv

            tmptime += (3600*24)

        if len(pricesshare) == 0:
            return

        name = Config.PRICES_PATH3 + S.id()
        json.dump(pricesshare, open(name,'w'))
        return

    def caculate(self, S, dt, p1, mv1, p, mv):
        T1 =  mv1/p1
        p2 = p
        T2 = mv/p

        delta = (T2 - T1)/T1
        ip2 = p1 / (1 + delta)

        prange = abs((p2 - ip2)/ip2)

        realprange = abs((p2 - p1)/p1)

        imv = int(mv/10000)
        if delta < 0.00001:     #share is not changed
            self._stats["same"] += 1
            return (p, 1, imv)

        if delta < 0.05:
            self._stats["minidelta"] += 1
            return (p, 1, imv)

        if abs(prange) < 0.20:  #allow change between +-20%
            self._stats["sendingshare"] += 1
#            tmp = delta - (1.0 * int(delta * 10) / 10)
#            if tmp < 0.001:
#                print delta, prange
            return (p, (1 + delta), imv)

        if realprange < 0.12: #增资扩股？
            self._stats["addshare"] += 1
            return (p, 1, imv)

#        print "left: ", S.id(), str(dt),  delta, prange, realprange
        self._stats["left"] += 1

        return (p, 0, 0)


    def date(self, dt):
        return (dt.year, dt.month, dt.day)
        pass
