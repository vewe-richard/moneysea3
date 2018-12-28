
import json
from moneyseav3.config import Config
from moneyseav3.fileparsers.recentprices import RecentPrices
from moneyseav3.fileparsers.historyprices import HistoryPrices

class Prices:
    def __init__(self):
        self._latestdate = "19000101"
        self._recentpricesdict = {}
        self._historypricesdict = {}
        self._historypricessharedict = {}
        self._hpssimplelist = {}

        rp = RecentPrices()
        for item in rp.listpricefiles():
            vals = item.split("-")
            date = vals[0]
            self._recentpricesdict[date] = vals[1]
            if date > self._latestdate:
                self._latestdate = date
        pass


    def price(self, stockid, date = None):  #date = (year, month, day)
        if date == None:
            datestr = self._latestdate
        else:
            datestr = "%02d%02d%02d"%date

        try:
            rp = self.getrecentprices(datestr)
            p = rp[stockid]
            return p
        except Exception as e:
            p = None
            pass

        #try find price from historyprices
        try:
            hp = self.gethistoryprices(stockid)
            key = "%02d-%02d-%02d"%date
            items = hp.getprices()[key]
            return float(items[0])
        except Exception as e:
            pass
        return p

    def historyprice(self, stockid, date):  #date = (year, month, day)
        #try find price from historyprices
        try:
            hp = self.gethistoryprices(stockid)
            key = "%02d-%02d-%02d"%date
            items = hp.getprices()[key]
            return float(items[0])
        except Exception as e:
            return None

    def historymarketvalue(self, stockid, date):
        try:
            hp = self.gethistoryprices(stockid)
            key = "%02d-%02d-%02d"%date
            items = hp.getprices()[key]
            return float(items[1])
        except Exception as e:
            return None

    def historyrange(self, stockid):
        try:
            hp = self.gethistoryprices(stockid)
            return hp.range()
        except Exception as e:
            return None

    def gethistoryprices(self, stockid):
        try:
            hp = self._historypricesdict[stockid]
        except:
            hp = HistoryPrices(stockid)
            self._historypricesdict[stockid] = hp
        return hp

    def getrecentprices(self, date):
        rp = self._recentpricesdict[date]
        if type(rp) is str: #need loading it from files
            rlt = self.recentload(date, rp)
            self._recentpricesdict[date] = rlt
        return self._recentpricesdict[date]

    def recentload(self, date, rp):
        filepath = Config.PRICES_PATH + "/" + date + "-" + rp
        p = json.load(open(filepath))
        return p

    def historypricesshare(self, sid, date):
        key = "%02d-%02d-%02d"%date
        hps = self.gethistorypricessharedict(sid)
        
        try:
            return hps[key]
        except:
            return None

    def gethistorypricessharedict(self, sid):
        try:
            hps = self._historypricessharedict[sid]
        except:
            try:
                filepath = Config.PRICES_PATH3 + "/" + sid
                hps = json.load(open(filepath))
                self._historypricessharedict[sid] = hps
            except:
                hps = None
                self._historypricessharedict[sid] = hps
                return None
            pass
        return hps


    def gethpssimplelist(self, sid):
        hpsl = None
        try:
            hpsl = self._hpssimplelist[sid]
        except:
            hps = self.gethistorypricessharedict(sid)
            if hps == None:
                return None

            start = "9999-99-99"
            end = "0000-00-00"
            
            sitem = None
            eitem = None
            ll = []

            for k in hps.keys():
                cnt = hps[k]

                if k > end:
                    eitem = (k, cnt)
                    end = k
                if k < start:
                    sitem = (k, cnt)
                    start = k

                if cnt[1] != 1:
                    ll.append((k, cnt))
            hpsl = sorted(ll, key=lambda x: x[0])


            if len(hpsl) == 0 or hpsl[0][0] > sitem[0]:
                hpsl.insert(0, sitem)
            if hpsl[-1][0] < eitem[0]:
                hpsl.append(eitem)
        return hpsl

if __name__ == "__main__":
    ps = Prices()
    print ps.price("300230", (2018, 11, 28))
    print ps.marketvalue("300230", (2018, 11, 28))
    print ps.historyrange("300230")

    pass










