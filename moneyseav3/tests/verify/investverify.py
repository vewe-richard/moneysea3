from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
from moneyseav3.invest.investone import InvestOne

class InvestVerify(BaseTestUnit):
    def cmd(self):
        return "invest"

    def summary(self):
        return "verify invest comparing to holded records"

    def run(self, args, opts):
        gbls = Globals.get_instance()
        ohr1 = gbls.oneholdedrecord("input/holded/holded-20181110-0930")
        ohr2 = gbls.oneholdedrecord("input/holded/holded-20181120-1330")

        for s in ohr2.stocks():
            if ohr2.gettotal(s) < 1:
                continue
            if not s in ohr1.stocks():
                continue

            if not ohr1.gettotalholded(s) == ohr2.gettotalholded(s):
                continue
                
            print s, ohr1.gettotal(s), ohr1.getprice(s), ohr1.gettotalholded(s)
            print s, ohr2.gettotal(s), ohr2.getprice(s), ohr2.gettotalholded(s)
            stock = gbls.getstock(s)
            io = InvestOne(stock)
            io.buyshare(ohr1.gettotalholded(s), (2018, 11, 12))
            hps1 = stock.historypricesshare((2018,11,12))
            hps2 = stock.historypricesshare((2018,11,21))
            print s, hps1[0], hps2[0]

            money = io.sell((2018,11,21))
            delta1 = (ohr2.gettotal(s) - ohr1.gettotal(s))/ohr1.gettotal(s)
            delta2 = io.added()
            print s, delta1, delta2
            print ""

