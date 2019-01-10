# coding=utf-8
# 假定每年1月1日，对市面上的每只股票，都买入一份金额相等
# 画出一年之内，市值最高的点，和市值最低的点
# 这就意味着，过去多年，在最低点买入，最高点卖出，可获利
# 这是过去的统计，也对将来的行为产生指导意义
from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time
import matplotlib.pyplot as plt
import traceback

class BuySellDates(BaseTestUnit):
    DEBUG = False
    STARTYEAR = 2000
    ENDYEAR = 2019
    DAYS = 365 + 30

    def cmd(self):
        return "buyselldates"

    def summary(self):
        return "show good buy and sell dates for reference"

    def run(self, args, opts):
        self._db = {}
        self._ss = Globals.get_instance().stocks()
        for year in range(self.STARTYEAR, self.ENDYEAR + 1):
            ydb = {}
            sdt = self.startdate(year)
            dt = datetime.date(year, sdt[1], sdt[2])
            tmptime = time.mktime(dt.timetuple())
            ydb["starttime"] = tmptime
            self._db[year] = ydb
        #for every date
        cnt1 = 0
        ax = []
        ay = []
        for i in range(0, self.DAYS):
            cnt2 = 0
            total = 0
            for year in range(self.STARTYEAR, self.ENDYEAR):
                ydb = self._db[year]
                stime = ydb["starttime"]
                ttime = stime + (i * 3600 * 24)

                dt = datetime.date.fromtimestamp(ttime)
                ytotal = self.yeartotal(ydb, dt)
#                print dt, ydb, ytotal
#                print i, dt, ytotal
                total += ytotal
                cnt2 += 1
                if cnt2 > 1 and self.DEBUG:
                    break

            # corresponding to new year
            ttime = self._db[self.ENDYEAR]["starttime"] + (i * 3600 * 24)
            dt = datetime.date.fromtimestamp(ttime)
            if i == 0:
                inittotal = total
            delta = (total - inittotal)*100/total
            print i, dt, ":(%6.2f, %6.2f)"%(total, delta), "%"
            ax.append(i)
            ay.append(delta)
 
            cnt1 += 1
            if cnt1 > 1 and self.DEBUG:
                break

        plt.plot(ax, ay, color="red", linewidth=2)
        #make a reference
        ax = []
        ay = []
        ax.append(365)
        ay.append(20)
        ax.append(365)
        ay.append(-20)
        plt.plot(ax, ay, color="black", linewidth=2)
        ax = []
        ay = []
        ax.append(0)
        ay.append(0)
        ax.append(self.DAYS)
        ay.append(0)
        plt.plot(ax, ay, color="black", linewidth=2)
        #index 28, Feb 1
        ax = []
        ay = []
        ax.append(28)
        ay.append(-5)
        ax.append(28)
        ay.append(5)
        plt.plot(ax, ay, color="blue", linewidth=2)
        #index 97, April 10
        ax = []
        ay = []
        ax.append(97)
        ay.append(-5)
        ax.append(97)
        ay.append(5)
        plt.plot(ax, ay, color="blue", linewidth=2)
        #index 160, June 12
        ax = []
        ay = []
        ax.append(160)
        ay.append(-5)
        ax.append(160)
        ay.append(5)
        plt.plot(ax, ay, color="blue", linewidth=2)

        ax = []
        ay = []
        ax.append(250)
        ay.append(-5)
        ax.append(250)
        ay.append(5)
        plt.plot(ax, ay, color="blue", linewidth=2)

        plt.show()
        return

    def yeartotal(self, ydb, dt):
        try:
            stocks = ydb["stocks"]
            total = self.caculate(ydb, dt)
            return total
        except KeyError as e:
#            print traceback.format_exc()
            total = self.buy(ydb, dt)
            return total

    def caculate(self, ydb, dt):
        stocks = ydb["stocks"]
        total = 0
        for idx in stocks:
            mv = stocks[idx]
            S = self._ss[idx]
            hps = S.historypricesshare((dt.year, dt.month, dt.day))
            if hps == None:
#                print "for hps is None:", mv[1]
                total += mv[1]
                continue
            share = mv[0] * hps[1]
            value = share * hps[0]
            stocks[idx] = (share, value)
            total += value
        return total

    def buy(self, ydb, dt):
        cnt = 0
        total = 0
        stocks = {}
        for idx in self._ss:
            S = self._ss[idx]
            hps = S.historypricesshare((dt.year, dt.month, dt.day))
            if hps == None:
                continue
            share = 100/hps[0]
            stocks[idx] = (share, 100)
            total += 100

            cnt += 1
            if cnt > 1 and self.DEBUG:
                break
        ydb["stocks"] = stocks
        return total

    def startdate(self, year):
        return self.noweekend(year, 1, 4)  #start from Jan 4

    def noweekend(self, year, month, day):
        dt = datetime.date(year, month, day)
        tmptime = time.mktime(dt.timetuple())
        ndt = datetime.date.fromtimestamp(tmptime)
        if ndt.weekday() == 5 or ndt.weekday() == 6:
            tmptime += (3600 * 24) * (7 - ndt.weekday())
            ndt = datetime.date.fromtimestamp(tmptime)
        return (ndt.year, ndt.month, ndt.day)












