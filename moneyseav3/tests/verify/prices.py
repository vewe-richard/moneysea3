from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit

class PricesVerify(BaseTestUnit):
    PRICE_ZERO = 0.00001
    def cmd(self):
        return "prices"

    def summary(self):
        return "verify prices data, and the resources.Prices class. By comparing prices between recent and history prices file "

    def run(self, args, opts):
        gbls = Globals.get_instance()
        fails = 0
        for s in gbls.stocks():
            S = gbls.stocks()[s]
            recent = S.price((2018,11,30))
            history = S.price((2018,11,29))
            if self.zero(recent) and self.zero(history):
                continue

            if self.zero(recent) or self.zero(history):
                print s, recent, history
                fails += 1
                continue

            delta = (recent - history)/history
            if abs(delta) > 0.10:
                print s, delta
                fails += 1
                continue

        delta = (fails * 1.0) / len(gbls.stocks())
        print "Mismatch ratio: ", delta * 100, "%"
        if delta < 0.1:
            self._result = True
        else:
            self._result = False


    def zero(self, value):
        if value == None or value < self.PRICE_ZERO:
            return True

        return False
