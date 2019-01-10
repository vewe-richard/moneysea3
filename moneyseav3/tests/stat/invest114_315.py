# coding=utf-8
from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time
import operator

from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

class Invest114_315(BaseTestUnit):
    STARTY = 2005
    ENDY = 2018
    STARTDATE = (1, 14)
    ENDDATE = (3, 15)
    DEBUG = True

    def cmd(self):
        return "114_315"

    def summary(self):
        return "statistics of addings for stocks from 1.14 to 3.15 every year"

    def select(self):
        for start in range(16, 30):
            for end in range(1, 15):
                print "1", start, " --- ", "3", end

    def run(self, args, opts):
        cmds = {"trend": self.trend, "select": self.select}
        func = None
        for k in cmds:
            if k == args[0]:
                func = cmds[k]
                break
        if func == None:
            print "allow commands: ", cmds.keys()
            return

        if args[0] == "select":
            self.select()
            return

        starty = self.STARTY
        endy = self.ENDY
        self.caculateaddings(starty, endy, func)

    def caculateaddings(self, starty, endy, func):
        self._ss = Globals.get_instance().stocks()
        print "total samples:", (endy - starty) * len(self._ss) / 2
        ys = {}
        cnt = 0
        for y in range(starty, endy):
            yp = self.yearprocess(y)
            ys[y] = yp
            if cnt > 1 and self.DEBUG:
                break
            cnt += 1
        func(ys)

    def trend(self, ys):
        stats = {}
        for x in range(0, 21):
            ratio = x*0.1 - 1
            stats[str(ratio)] = 0
        total = 0
        earning = 0
        loss = 0
        for y in range(self.STARTY, self.ENDY):
            try:
                yl = ys[y]
            except:
                continue

            for s in yl:
                idx = int((s[1] + 1.0)/0.1 + 0.5)
                if idx < 0:
                    idx = 0
                if idx > 20:
                    idx = 20
                k = (idx - 10)/10.0
                stats[str(k)] += 1
                total += 1
                if k > 0.001:
                    earning += 1
                if k < -0.001:
                    loss += 1
            if self.DEBUG:
                break
        print "real samples:", total
        print stats
        print "earning: ", earning * 1.0/total, "loss:", loss * 1.0/total, "equal: ", stats["0.0"] * 1.0 / total
        ax = []
        ay = []
        for x in range(0, 21):
            ratio = x*0.1 - 1
            ax.append(ratio)
            ay.append(stats[str(ratio)] * 1.0/total)
        plt.plot(ax, ay, color="red", linewidth=2)
        plt.show()
 

        

    def yearprocess(self, year):
        # caculate suitable start date and end date
        sdt = datetime.date(year, self.STARTDATE[0], self.STARTDATE[1])
        tmptime = time.mktime(sdt.timetuple())
        nsdt = datetime.date.fromtimestamp(tmptime)
        if nsdt.weekday() == 5 or nsdt.weekday() == 6:
            tmptime += (3600 * 24) * (7 - nsdt.weekday())
            nsdt = datetime.date.fromtimestamp(tmptime)

        edt = datetime.date(year, self.ENDDATE[0], self.ENDDATE[1])
        tmptime = time.mktime(edt.timetuple())
        nedt = datetime.date.fromtimestamp(tmptime)
        if nedt.weekday() == 5 or nedt.weekday() == 6:
            tmptime += (3600 * 24) * (7 - nedt.weekday())
            nedt = datetime.date.fromtimestamp(tmptime)

        # for every stock, get price on 1.14 and price on 3.15
        ass = {}
        cnt = 0
        for s in self._ss:
            S = self._ss[s]
            ad = self.adding(S, (nsdt.year, nsdt.month, nsdt.day), (nedt.year, nedt.month, nedt.day))
            if ad == None:
                continue
            ass[s] = ad

            if cnt > 10 and self.DEBUG:
                break
            cnt += 1
        sitems = sorted(ass.items(), key=operator.itemgetter(1))
        return sitems

    def adding(self, S, sdt, edt):
        shps = S.historypricesshare(sdt)
        ehps = S.historypricesshare(edt)
        if shps == None or ehps == None:
            return None
        ad = (ehps[0] - shps[0])/shps[0]
        return ad

