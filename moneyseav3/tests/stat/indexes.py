
class BaseIndex:
    def name(self):
        return "base"
    def value(self):
        return 0
    def setup(self, start, end, s, reportseason = None):
        self._start = start
        self._end = end
        self._s = s
        self._reportseason = reportseason
        pass

class GainIndex(BaseIndex):
    def name(self):
        return "gain"
    def value(self):
        #start price
        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None

        #end price
        hps2 = self._s.validhistorypricesshare(self._end, 15)
        if hps2 == None:
            return None

        try:
            share = (hps2[2]/hps2[0])/(hps[2]/hps[0])
        except:
            print "Discard for can not caculate share for gain index:", self._s.name(), self._start, self._end, (hps2[2], hps2[0]), (hps[2], hps[0])
            return None
        gain = (share * hps2[0])/(hps[0]) - 1
        return gain

class PriceIndex(BaseIndex):
    def value(self):
        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None
        return hps[0]

    def name(self):
        return "price"

class PriceDeltaIndex(BaseIndex):
    def value(self):
        hps0 = self._s.validhistorypricesshare(self._start, 15)
        hps1 = self._s.validhistorypricesshare(self._end, 15)

        if hps0 == None or hps1 == None:
            return None

        try:
            share = (hps1[2]/hps1[0])/(hps0[2]/hps0[0])
        except:
            return None

        gain = (share * hps1[0])/(hps0[0]) - 1
        return gain

    def name(self):
        return "pricedelta"

class MarketValueIndex(BaseIndex):
    def value(self):
        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None
        return hps[2]

    def name(self):
        return "marketvalue"

class NegativeMarketValueIndex(BaseIndex):
    def value(self):
        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None
        return (0 - hps[2])

    def name(self):
        return "negativemarketvalue"

class ReportIndex(BaseIndex):
    def __init__(self, tag):
        self._tag = tag
        pass
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] + self._reportseason[0], self._reportseason[1])
        try:
            p = r[self._tag]
        except:
            return None
        return p

    def name(self):
        return "report." + self._tag + "_" + str(self._reportseason[1])

class PseYieldIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] + self._reportseason[0], self._reportseason[1])
        try:
            p = r["per_share_earnings"]
        except:
            return None
        if p == None:
            return None

        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None

        return p/hps[0]


    def name(self):
        return "pse_yield"

class EQRatio(BaseIndex):
    def __init__(self, tag):
        self._tag = tag
        pass
    def value(self):
        fd = self._s.fd()
        r = fd.report(self._start[0] + self._reportseason[0], self._reportseason[1])
        try:
            a = r[self._tag] / 100
            e = r["per_share_earnings"]
        except Exception as e:
            return None
        if a == None:
            return None
        if e == None:
            return None

        if e < 0.0001:
            return None
        if abs(a + 1) < 0.000001:
            a = -0.99999

        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None


        n = 5
        p = 0.08
        eq = (((p+1)/(a+1))**n) * p  #------ (2)
        q = e/eq

        dratio = (q - hps[0])/hps[0]
        return dratio


    def name(self):
        return "eqratio_" + self._tag

class RangeAdding(BaseIndex):
    def __init__(self, tag, yrange):
        self._tag = tag
        self._yrange = yrange
        pass
    def value(self):
        fd = self._s.fd()
        if self._yrange > 0:
            start = self._start[0]
            end = self._start[0] + self._yrange
        else:
            end = self._start[0]
            start = self._start[0] + self._yrange

        rstart = fd.report(start + self._reportseason[0], self._reportseason[1])
        rend = fd.report(end + self._reportseason[0], self._reportseason[1])
        try:
            delta = (rend[self._tag] - rstart[self._tag]) / rstart[self._tag]
        except:
            return None
        return delta


    def name(self):
        return "ra_" + self._tag + "_" + str(self._yrange)

class EQRangeAdding(BaseIndex):
    def __init__(self, tag, yrange, refpricedate = None):
        self._tag = tag
        self._yrange = yrange
        self._refpricedate = refpricedate
        pass
    def value(self):
        fd = self._s.fd()
        if self._yrange > 0:
            start = self._start[0]
            end = self._start[0] + self._yrange
        else:
            end = self._start[0]
            start = self._start[0] + self._yrange

        rstart = fd.report(start + self._reportseason[0], self._reportseason[1])
        rend = fd.report(end + self._reportseason[0], self._reportseason[1])
        try:
            delta = (rend[self._tag] - rstart[self._tag]) / rstart[self._tag]

            a = delta
            e = rstart["per_share_earnings"]
        except:
            return None

        if a == None:
            return None
        if e == None:
            return None

        if e < 0.0001:
            return None
        if abs(a + 1) < 0.000001:
            a = -0.99999

        if self._refpricedate == None:
            hps = self._s.validhistorypricesshare(self._start, 15)
            if hps == None:
                return None
        else:
            p = self._s.price(self._refpricedate)
            if p == None:
                return None
            hps = (p, 0)


        n = 5
        p = 0.08
        eq = (((p+1)/(a+1))**n) * p  #------ (2)
        q = e/eq

        dratio = (q - hps[0])/hps[0]

        '''
        print "stock:", self._s.id()
        print "eq:", eq
        print "adding:", a
        print "price:", hps[0]
        print "earning:", e
        '''
        return dratio


    def name(self):
        return "eqra_" + self._tag + "_" + str(self._yrange)


class EQPrevAdding(BaseIndex):
    def __init__(self, tag, yrange, refpricedate = None):
        self._tag = tag
        self._yrange = yrange
        self._refpricedate = refpricedate
        pass
    def value(self):
        fd = self._s.fd()
        if self._yrange > 0:
            start = self._start[0]
            end = self._start[0] + self._yrange
        else:
            end = self._start[0]
            start = self._start[0] + self._yrange

        rstart = fd.report(start + self._reportseason[0], self._reportseason[1])
        rend = fd.report(start + self._reportseason[0] + 1, self._reportseason[1])
        try:
            delta = (rend[self._tag] - rstart[self._tag]) / rstart[self._tag]

            a = delta
            e = rstart["per_share_earnings"]
        except:
            return None

        if a == None:
            return None
        if e == None:
            return None

        if e < 0.0001:
            return None
        if abs(a + 1) < 0.000001:
            a = -0.99999

        if self._refpricedate == None:
            hps = self._s.validhistorypricesshare(self._start, 15)
            if hps == None:
                return None
        else:
            p = self._s.price(self._refpricedate)
            if p == None:
                return None
            hps = (p, 0)

        n = 5
        p = 0.08
        eq = (((p+1)/(a+1))**n) * p  #------ (2)
        q = e/eq

        dratio = (q - hps[0])/hps[0]

        return dratio


    def name(self):
        return "eqpa_" + self._tag + "_" + str(self._yrange)




if __name__ == "__main__":
    from moneyseav3.globals import Globals

    s = Globals.get_instance().getstock("300230")

#    I = MarketValueIndex() #PriceIndex() #GainIndex() # BaseIndex(), 
#    I = PseYieldIndex((2018, 2))
    I = EQRatio("profit_adding")
    I.setup((2019, 2, 22), None, s, (-1, 2))
    print I.value()

'''
    I = RangeAdding("profit", -2)
    I.setup((2015, 11, 20), (2018, 11, 20), s)
    print I.name()
    print I.value()
    reporttags = ("per_share_earnings", "per_share_asset", "per_share_cash2", "sales", 
            "msales_profit", "sales_profit", "invest_gain", "other_gain", 
            "total_profit", "profit", "profit2", "total_cash", "cach_adding", 
            "total_asset", "flow_asset", "total_debt", "flow_debt",
            "rights", "asset_yield", "profit_adding", "profit2_adding", "sales_adding")
    for tag in reporttags:
        I = ReportIndex((2018, 2), tag)
        I.setup((2017, 11, 20), (2018, 11, 20), s)
        print I.name()
        print I.value()
'''
