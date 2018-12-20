# coding=utf-8
from moneyseav3.config import Config

class HistoryPrices:
    def getprices(self, stockid):
        path = Config.PRICES_PATH2 + "/" + stockid + ".csv"
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
                    mydict[vals[0]] = (vals[3], vals[13]) #当日收盘价和总市值
            return mydict
        except:
            return None

if __name__ == "__main__":
    from moneyseav3.globals import Globals

    allstocks = Globals.get_instance().stocks().keys()
    for idx in allstocks:
        hp = HistoryPrices()
        dct = hp.getprices(idx)
#        print idx, len(dct)

