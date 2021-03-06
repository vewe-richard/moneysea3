# coding=utf-8
from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
from moneyseav3.tests.stat.basestat import BaseStat
from moneyseav3.resources.stock import Stock
from moneyseav3.tests.stat.drawstat import DrawStat


class HS300(BaseTestUnit):
    def cmd(self):
        return "hs300"

    def summary(self):
        return "draw 沪深300收益率，和招商证券的曲线对比"

    def run(self, args, opts):
        hss = HS300Stat((2018, 11, 1), (2018, 12, 31))
        shs = SHAStat((2018, 11, 1), (2018, 12, 31))
        szs = SZStat((2018, 11, 1), (2018, 12, 31))

        ds = DrawStat([hss.addings(), shs.addings(), szs.addings()])
        ds.draw()


        pass
 


class HS300Stat(BaseStat):
    def __init__(self, start, end):
        BaseStat.__init__(self, start, end)

        idx = "0000300"
        self._S = Stock(Globals.get_instance(), idx)
        pass

    def price(self, date):
        return self._S.price(date)

class SHAStat(BaseStat):
    def __init__(self, start, end):
        BaseStat.__init__(self, start, end)

        idx = "0000001"
        self._S = Stock(Globals.get_instance(), idx)
        pass

    def price(self, date):
        return self._S.price(date)

class SZStat(BaseStat):
    def __init__(self, start, end):
        BaseStat.__init__(self, start, end)

        idx = "1399001"
        self._S = Stock(Globals.get_instance(), idx)
        pass

    def price(self, date):
        return self._S.price(date)
