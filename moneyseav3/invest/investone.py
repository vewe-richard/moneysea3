from moneyseav3.globals import Globals
import datetime, time

class InvestOne:
    def __init__(self, stock):
        self._s = stock
        self._share = 0
        pass

    def buy(self, money, date):
        self._buydate = date
        hps = self._s.historypricesshare(date)
        if hps == None:
            raise Exception("Can not buy stock " + self._s.id() + " on " + self.strdate(date))
        p = hps[0]
        self._initshare = int(money / (100*p)) * 100
        self._share = self._initshare
        self._valueonbuy = self._share * p
        return (money - self._valueonbuy)

    def sell(self, date):
        hps = self._s.historypricesshare(date)
        if hps == None:
            raise Exception("Can not sell stock " + self._s.id() + " on " + self.strdate(date))

        #setaccountdate, caculate the new share
        self.setaccountdate(date)
        #caculate money
        money = self.value()
        self._share = 0
        return money

    def setaccountdate(self, date):
        startstr = self.strdate(self._buydate)
        endstr = self.strdate(date)

        self._share = self._initshare
        for item in self._s.gethpssimplelist():
#            print item[0], item[1][1], startstr, endstr
            if item[0] <= startstr:
                continue
            if item[0] > endstr:
                break
            sending = item[1][1]
            self._share *= sending

        #set account date
        dt = datetime.date(date[0], date[1], date[2])

        tmptime = time.mktime(dt.timetuple())
        while True:
            ndt = datetime.date.fromtimestamp(tmptime)
            hps = self._s.historypricesshare((ndt.year, ndt.month, ndt.day))
            if hps != None:
                break
            tmptime -= (3600*24)
        self._accountdate = (ndt.year, ndt.month, ndt.day)
        self._accountvalue = self._share * hps[0]
        pass

    def share(self):
        return int(self._share)

    def valueonbuy(self):
        return self._valueonbuy

    def value(self):
        return int(self._accountvalue)

    #added percent comparing to initial value
    def added(self):
        return (self._accountvalue - self._valueonbuy)/self._valueonbuy

    def strdate(self, date):
        return "%02d-%02d-%02d"%date



if __name__ == "__main__":
    gbls = Globals.get_instance()
    S = gbls.getstock("002061")
#    S = gbls.getstock("300230")
#    S = gbls.getstock("601318")
    io = InvestOne(S)
    left = io.buy(20000, (2011, 11, 25))

    print "Buy > ", S.id()
    print "Left: ", left
    print "share: ", io.share(), "valueonbuy: ", io.valueonbuy()

    io.setaccountdate((2018, 11, 28))

    print "Account >"
    print "share: ", io.share(), "value: ", io.value()
    print "added: ", io.added()

    money = io.sell((2018, 11, 28))
    print "Sell >"
    print "money: ", money








