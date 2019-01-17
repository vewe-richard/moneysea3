from moneyseav3.tests.basetestaction import BaseTestAction
from moneyseav3.tests.stat.hs300 import HS300
from moneyseav3.tests.stat.drawylgf import DrawYlgf
from moneyseav3.tests.stat.invest114_315 import Invest114_315
from moneyseav3.tests.stat.buyselldates import BuySellDates
from moneyseav3.tests.stat.relatedindexes import RelatedIndexes


class StatAction(BaseTestAction):
    def __init__(self):
        self._actions = [HS300, DrawYlgf, Invest114_315, BuySellDates, RelatedIndexes]
        pass

    def cmd(self):
        return "stat"

    def summary(self):
        return "statistics on history prices, to investigate adding relative index"

