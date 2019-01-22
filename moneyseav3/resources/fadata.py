from moneyseav3.config import Config
from moneyseav3.fileparsers.ffnetease import FFNetEase
from moneyseav3.fileparsers.ff10jqka import FF10jqka

class FaData:
    NETEASE = 1
    TONGHS = 2
    def __init__(self, stockid, source = None):        # consturct from FFNetease, if not suitable, consturct from 10jqka
        if source == None:
            source = self.NETEASE

        self._ff = None
        if source == self.TONGHS:
            from moneyseav3.globals import Globals
            path = Globals.get_instance().getff10jqka().getpath(stockid) + "/finance"
            self._ff = FF10jqka(path)
            self._ff.doparse()
        else:           #netease
            self._ff = FFNetEase(Config.STOCKS_PATH_NETEASE + "/zycwzb_" + stockid + ".html?type=report")
            self._ff.doparse()
            pass
        pass

    def yearreport(self, year): # return dict
        return self.report(year, 3)

    def report(self, year, season):
        if self._ff == None:
            return None
        return self._ff.report(year, season)

    def latest(self):         # (year, season)
        if self._ff == None:
            return None
        r = self.latestreport()
        return (r["year"], r["season"])

    def oldest(self):         # (year, season)
        if self._ff == None:
            return None
        r = self.oldestreport()
        return (r["year"], r["season"])

    def all(self):            # list of all valid reports
        if self._ff == None:
            return None
        return self._ff.allreports()

    def latestreport(self):   # latest report
        if self._ff == None:
            return None
        return self._ff.latestreport()

    def oldestreport(self):   # oldest report
        if self._ff == None:
            return None
        return self._ff.oldestreport()
 

if __name__ == "__main__":

    fd = FaData("600671", source=FaData.NETEASE)
    r = fd.report(2017, 2)
    print r
    r = fd.report(2016, 2)
    print r

