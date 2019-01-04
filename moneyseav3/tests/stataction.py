from moneyseav3.tests.basetestaction import BaseTestAction
from moneyseav3.tests.stat.hs300 import HS300
from moneyseav3.tests.stat.drawylgf import DrawYlgf


class StatAction(BaseTestAction):
    def __init__(self):
        self._actions = [HS300, DrawYlgf]
        pass

    def cmd(self):
        return "stat"

    def summary(self):
        return "statistics on history prices, to investigate adding relative index"

