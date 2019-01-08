# coding=utf-8
from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time

class Invest114_315(BaseTestUnit):
    STARTY = 2005
    ENDY = 2018
    STARTDATE = (1, 14)
    ENDDATE = (3, 15)

    def cmd(self):
        return "114_315"

    def summary(self):
        return "statistics of addings for stocks from 1.14 to 3.15 every year"

    def run(self, args, opts):

        self._ss = Globals.get_instance().stocks()
        starty = self.STARTY
        endy = self.ENDY

        print "total samples:", (endy - starty) * len(self._ss) / 2
        for y in range(starty, endy):
            self.yearprocess(y)
        pass

    def yearprocess(self, year):
        # caculate suitable start date and end date
        dt = datetime.date(year, self.STARTDATE[0], self.STARTDATE[1])
        tmptime = time.mktime(dt.timetuple())
        ndt = datetime.date.fromtimestamp(tmptime)
        print ndt

        # for every stock, get price on 1.14 and price on 3.15
        for s in self._ss:
            S = self._ss[s]
            self.adding(S)
            break
        pass

    def adding(self, S):
        print S.historypricesshare((2017, 1, 16))

