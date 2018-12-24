from moneyseav3.actions.baseaction import BaseAction
from moneyseav3.globals import Globals
import datetime, time

class TotalShares(BaseAction):
    def cmd(self):
        return "totalshares"

    def summary(self):
        return "verify total shares"

    def run(self, args, opts):
        gbls = Globals.get_instance()
        for s in gbls.stocks():
            S = gbls.stocks()[s]
            self.verifytotalshares(S)
            break

    def verifytotalshares(self, S):
        rng = S.historypricesrange()
        startstr = rng[0]
        endstr = rng[1]

        items = startstr.split("-")

        startdate = datetime.date(int(items[0]), int(items[1]), int(items[2]))
        tmptime = time.mktime(startdate.timetuple())
        while True:
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break
            p = S.historyprice(self.date(dt))
            mv = S.historymarketvalue(self.date(dt))
            if p == None or mv == None:
                tmptime += (3600*24)
                continue
            if p < 0.00001:
                tmptime += (3600*24)
                continue
            
            print  S.id(), str(dt), p, mv, mv/p
            tmptime += (3600*24)
        return

    def date(self, dt):
        return (dt.year, dt.month, dt.day)

    def run2(self, args, opt):
        ts = time.time()
        dt = datetime.date.fromtimestamp(ts)
        print dt
        pass


