# coding=utf-8
from moneyseav3.config import Config

class HistoryPrices:
    def __init__(self, stockid):
        mydict = None
        path = Config.PRICES_PATH2 + "/" + stockid + ".csv"
        start = "9999-99-99"
        end = "0000-00-00"
        try:
            mydict = {}
            with open(path) as f:
                for line in f:
                    vals = line.split(",")
                    if len(vals) < 2:
                        continue
                    if len(vals) < 16:
                        print "Error:" + line
                        continue
                    if not self.validdate(vals[0]):
                        continue
                    mydict[vals[0]] = (vals[3], vals[13]) #当日收盘价和总市值
                    if vals[0] < start:
                        start = vals[0]
                    if vals[0] > end:
                        end = vals[0]
        except Exception as e:
            pass
        self._mydict = mydict
        self._range = (start, end)

    def getprices(self):
        return self._mydict

    def range(self):
        return self._range

    def validdate(self, dstr):
        items = dstr.split("-")
        if len(items) != 3:
            return False
        return True

if __name__ == "__main__2":
    from moneyseav3.globals import Globals

    allstocks = Globals.get_instance().stocks().keys()
    for idx in allstocks:
        hp = HistoryPrices(idx)
        dct = hp.getprices()
        print dct
        print idx, len(dct)
        print hp.range()
        break

if __name__ == "__main__":
    idx = "0000001"
    hp = HistoryPrices(idx)
    dct = hp.getprices()
    print dct
    print idx, len(dct)
    print hp.range()
