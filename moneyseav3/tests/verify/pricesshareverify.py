from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time

class PricesShareVerify(BaseTestUnit):
    PRICE_ZERO = 0.00001

    def cmd(self):
        return "pricesshare"

    def summary(self):
        return "verify pricesshare data"

    def run(self, args, opts):
        gbls = Globals.get_instance()
        fails = 0
        for s in gbls.stocks():
            S = gbls.stocks()[s]
            recent = S.price((2018,11,30))
            historyshare = S.historypricesshare((2018,11,29))
            if historyshare == None:
                continue
            history = historyshare[0]
            if self.zero(recent) and self.zero(history):
                continue

            if self.zero(recent) or self.zero(history):
                print s, recent, history
                fails += 1
                continue

            delta = (recent - history)/history
            if abs(delta) > 0.10:
                print s, delta
                fails += 1
                continue

        delta = (fails * 1.0) / len(gbls.stocks())
        print "Mismatch ratio: ", delta * 100, "%"
        if delta < 0.1:
            self._result = True
        else:
            self._result = False


    def zero(self, value):
        if value == None or value < self.PRICE_ZERO:
            return True

        return False

    def run1(self, args, opts):
        gbls = Globals.get_instance()
        sid = "300230"
        S = gbls.stocks()[sid]

        startstr = "2010-01-01"
        endstr = "2018-11-30"
        items = startstr.split("-")
        try:
            startdate = datetime.date(int(items[0]), int(items[1]), int(items[2]))
        except:
            #without correct history prices
            return
        tmptime = time.mktime(startdate.timetuple())

        while True:
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break

            p = S.historyprice(self.date(dt))
            ps = S.historypricesshare(self.date(dt))
            if (p == None or p < 0.001) and ps == None:
                tmptime += (3600*24)
                continue

            if p == None or ps == None:
                print "Warning: not match", p, ps
                tmptime += (3600*24)
                continue

            delta = (ps[0] - p)/p
            if delta < 0.00001:
                tmptime += (3600*24)
                continue
            print "Warning: mismatch"

            tmptime += (3600*24)

    def date(self, dt):
        return (dt.year, dt.month, dt.day)






