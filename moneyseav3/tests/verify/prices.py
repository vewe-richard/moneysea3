from moneyseav3.actions.baseaction import BaseAction
from moneyseav3.globals import Globals

class PricesVerify(BaseAction):
    def cmd(self):
        return "prices"

    def summary(self):
        return "verify prices data, and the resources.Prices class. By comparing prices between recent and history prices file "

    def run(self, args, opts):
        gbls = Globals.get_instance()
        for s in gbls.stocks():
            S = gbls.stocks()[s]
            recent = S.price((2018,11,30))
            history = S.price((2018,11,28))
            if recent == None or history == None:
                print s, recent, history
                continue

            if recent < 0.00001 or history < 0.00001:
                print s, recent, history
                continue

            delta = (recent - history)/history
            if abs(delta) > 0.11:
                print s, delta
