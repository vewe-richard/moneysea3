# coding=utf-8
from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
from moneyseav3.tests.stat.basestat import BaseStat
from moneyseav3.resources.stock import Stock
import datetime, time

from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

class HS300(BaseTestUnit):
    def cmd(self):
        return "hs300"

    def summary(self):
        return "draw 沪深300收益率，和招商证券的曲线对比"

    def run(self, args, opts):
        hss = HS300Stat((2018, 12, 3), (2018, 12, 31))

        ax = []
        ay = []
        count = 0
        ads = hss.addings()
        for a in ads:
            ax.append(count)
            ay.append(ads[count])
            count += 1

        print ax
        print ay
        plt.scatter(ax, ay, color='blue')
        plt.show()
        pass
 


class HS300Stat(BaseStat):
    def __init__(self, start, end):
        BaseStat.__init__(self, start, end)

        idx = "0000300"
        self._S = Stock(Globals.get_instance(), idx)
        
        self._startp = self._S.price(start)
        pass

    def price(self, date):
        return self._S.price(date)

    def addings(self):
        try:
            startdate = datetime.date(self._start[0], self._start[1], self._start[2])
        except:
            return None

        tmptime = time.mktime(startdate.timetuple())
        endstr = "%04d-%02d-%02d"%(self._end[0], self._end[1], self._end[2])
        al = []
        while True:
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break

            refp = self.price((dt.year, dt.month, dt.day))
            if refp != None:
                adding = (refp - self._startp)/self._startp
                al.append(adding)
            tmptime += (3600*24)
        return al
