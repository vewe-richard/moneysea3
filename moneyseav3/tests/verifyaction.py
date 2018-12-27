from moneyseav3.tests.basetestaction import BaseTestAction
from moneyseav3.tests.verify.prices import PricesVerify
from moneyseav3.tests.verify.totalshares import TotalShares
from moneyseav3.tests.verify.pricesshareverify import PricesShareVerify

class VerifyAction(BaseTestAction):
    def __init__(self):
        self._actions = [PricesVerify, PricesShareVerify, TotalShares]
        pass

    def cmd(self):
        return "verify"

    def summary(self):
        return "perform verifying"

