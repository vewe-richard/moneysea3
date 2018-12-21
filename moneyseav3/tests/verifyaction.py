from moneyseav3.tests.basetestaction import BaseTestAction
from moneyseav3.tests.verify.prices import PricesVerify

class VerifyAction(BaseTestAction):
    def __init__(self):
        self._actions = [PricesVerify]
        pass

    def cmd(self):
        return "verify"

    def summary(self):
        return "perform verifying"

