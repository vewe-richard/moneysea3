from moneyseav3.tests.basetestaction import BaseTestAction
from moneyseav3.tests.stat.hs300 import HS300


class StatAction(BaseTestAction):
    def __init__(self):
        self._actions = [HS300]
        pass

    def cmd(self):
        return "stat"

    def summary(self):
        return "statistics on history prices, to investigate adding relative index"

