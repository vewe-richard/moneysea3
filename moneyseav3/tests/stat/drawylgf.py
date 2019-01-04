# coding=utf-8
from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
from moneyseav3.tests.stat.basestat import BaseStat
from moneyseav3.resources.stock import Stock
from moneyseav3.tests.stat.drawstat import DrawStat
from moneyseav3.tests.stat.groupprice import GroupPrice


class DrawYlgf(BaseTestUnit):
    def cmd(self):
        return "ylgf"

    def summary(self):
        return "draw ylgf 300230 in two ways, comparing them in 同花顺"

    def run(self, args, opts):
        hss = HS300Stat((2013, 11, 29), (2018, 12, 31))
        gys = GroupYlgfStat((2013, 11, 29), (2018, 12, 31))

        ds = DrawStat([hss.addings(), gys.addings()])
#        ds = DrawStat([gys.prices()])
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


class GroupYlgfStat(BaseStat):
    def __init__(self, start, end):
        BaseStat.__init__(self, start, end)

        self._gp = GroupPrice(("300230",), start, end)
        pass

    def price(self, date):
        return self._gp.price(date)
