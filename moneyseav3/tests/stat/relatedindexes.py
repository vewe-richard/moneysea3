# coding=utf-8
# 股票收益和哪些指标相关？
# 取某个时间段的股票，根据收益率排序，前一半算好，后一半算差
# 对于任意指标，排序，前部算好，后半部算差
# 如果好的收益率，比如80%具有好的某指标，则认为收益率和该指标相关。
# 算法：
# 输入：
#    历史数据范围，考察区域，指标列表
# 中间输出：
#    dict | stock id, year, index0 (value), index1(value) ...
# 最后输出：
#    dict | stock id, year, index0 (value, True), index1(value, True) ... True: 好的指标，False，差的指标
#    index0(80%), index1(20%), index2(50%) ...
#
# class IndexStats:
#       init: historydata range, parse range, index list
#       run()
# class BaseIndex:
#       init: date
#       name(), value()
#
#
# result
#            iss = IndexStats( ((2000, 1, 1), (2018, 11, 30)), ((0, 1, 23), (0, 5, 7)), (GainIndex, ProfitValueIndex))
# index  price 0.453812381248 --- 价格无关
# index  marketvalue 0.454033516678 --- 市值无关
# index  profitvalue 0.444710111726 --- 上年第三季度的利润无关
# index  sales_adding 0.507964677631 --- 无相关性
# index  profit2_adding 0.514261112606 --- 无相关性
# index  profit_adding 0.507917487484 --- 无相关性
# index  pse_yield 0.451281994019 --- 无相关性
# index  eqratio_profit2_adding 0.519180889072 --- 无关
# index  eqratio_profit_adding 0.502294872679
# index  eqratio_sales_adding 0.487897283357
#

from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time
import json

class IndexStats:
    DEBUG = False

    def __init__(self, historyused, parserange, indexs):
        self._hstart = historyused[0]
        self._hend = historyused[1]

        dt = datetime.date(self._hstart[0], self._hstart[1], self._hstart[2])
        self._htstart = time.mktime(dt.timetuple())

        dt = datetime.date(self._hend[0], self._hend[1], self._hend[2])
        self._htend = time.mktime(dt.timetuple())

        self._rstart = parserange[0]
        self._rend = parserange[1]
        self._indexs = indexs
        pass

    def run(self):
        count = 0
        years = {}
        for year in range(self._hstart[0], self._hend[0] + 1):
            print "get index from ", year
            start = (year, self._rstart[1], self._rstart[2])
            end = (year + self._rend[0], self._rend[1], self._rend[2])
            #for every stock
            ss = Globals.get_instance().stocks()
            count2 = 0
            thisyear = {}
            for s in ss:
                S = ss[s]
                ids = {}
                for index in self._indexs:
                    idx = index #()
                    idx.setup(start, end, S)
                    v = idx.value()
                    ids[idx.name()] = v
                thisyear[s] = ids
                count2 += 1
                if count2 > 7 and self.DEBUG:
                    break
#                    pass
            years[year] = thisyear
            count += 1
            if count > 2 and self.DEBUG:
                break
#        print years
        json.dump(years, open("output/temp/years",'w'))
        pass

class BaseIndex:
    def name(self):
        return "base"
    def value(self):
        return 0
    def setup(self, start, end, s):
        self._start = start
        self._end = end
        self._s = s
        pass

class GainIndex(BaseIndex):
    def name(self):
        return "gain"
    def value(self):
        #def historypricesshare(self, date):
        #def gethpssimplelist(self):

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
            print "Discard:", self._s.name(), self._start, self._end, (hps2[2], hps2[0]), (hps[2], hps[0])
            return None
        #self._s.gethpssimplelist()
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

class MarketValueIndex(BaseIndex):
    def value(self):
        hps = self._s.validhistorypricesshare(self._start, 15)
        if hps == None:
            return None
        return hps[2]

    def name(self):
        return "marketvalue"

class ProfitValueIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

#        print self._s.id(), self._start, self._start[0] - 1

        r = fd.report(self._start[0] - 1, 2)
        try:
            p = r["profit"]
        except:
            return None
        return p

    def name(self):
        return "profitvalue"

class ProfitAddingIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] - 1, 2)
        try:
            p = r["profit_adding"]
        except:
            return None
        return p

    def name(self):
        return "profit_adding"

class Profit2AddingIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] - 1, 2)
        try:
            p = r["profit2_adding"]
        except:
            return None
        return p

    def name(self):
        return "profit2_adding"

class SalesAddingIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] - 1, 2)
        try:
            p = r["sales_adding"]
        except:
            return None
        return p

    def name(self):
        return "sales_adding"

class PerSEarningIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] - 1, 2)
        try:
            p = r["per_share_earnings"]
        except:
            return None
        return p

    def name(self):
        return "per_share_earnings"

class PseYieldIndex(BaseIndex):
    def value(self):
        fd = self._s.fd()

        r = fd.report(self._start[0] - 1, 2)
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
        r = fd.report(self._start[0] - 1, 2)
        try:
            a = r[self._tag] / 100
            e = r["per_share_earnings"]
        except:
            return None
        if a == None:
            return None

#        return (1+a3)
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

#        print "adding, \tprice, \te, \tq \tdratio"
#        print a, hps[0], "\t", e, q, "\t", dratio

        return dratio


    def name(self):
        return "eqratio_" + self._tag


class ParseIndexes:
    DEBUG = False
    def run(self):
        ys = json.load(open("output/temp/years"))
        ids = self.indexes(ys)
        stats = {}
        for ID in ids:
            if ID == "gain":
                continue
            stats[ID] = {}

        for y in ys:
            ss = ys[y]
            for ID in ids:
                if ID == "gain":
                    continue
                rate = self.parse(y, ss, ID)
                if rate == None:
                    continue
                stats[ID][y] = rate
#            break #DEBUG

        f = open("output/temp/result", "w")
        for ID in ids:
            if ID == "gain":
                continue
            avg = self.average(stats[ID])
            print "index ", ID, avg
            print >> f, ID
            for y in sorted(stats[ID].keys()):
                print >> f, "\t", y, stats[ID][y]
        f.close()
        json.dump(stats, open("output/temp/result-json",'w'))


        pass

    def average(self, stats):
        total = 0
        count = 0
        for y in stats:
            total += stats[y][0]
            count += 1

        return total/count

    def indexes(self, ys):
        for y in ys:
            ss = ys[y]
            for s in ss:
                return ss[s].keys()

    def parse(self, year, ss, ID):
        lgain = []
        lid = []
        for s in ss:
            S = ss[s]
            if S["gain"] == None or S[ID] == None:
                continue
            lgain.append(S["gain"])
            lid.append(S[ID])
        slgain = sorted(lgain)
        slid = sorted(lid)
        sz = len(slgain)
        if sz < 200 and not self.DEBUG:
            print year, ID, "samples count is too small, discard"
            return None
        avggain = slgain[sz/2]
        avgid = slid[sz/2]

        goodgains = 0
        goodids = 0
        for s in ss:
            S = ss[s]
            gain = S["gain"]
            vid = S[ID]
            if gain == None or vid == None:
                continue
            if gain > avggain:
                goodgains += 1
                if vid > avgid:
                    goodids += 1

        rate = goodids * 1.0 / goodgains
        return (rate, avggain, avgid)

class Parse2Indexes:
    DEBUG = False
    def run(self):
        ys = json.load(open("output/temp/years"))
        stats = json.load(open("output/temp/result-json"))
        for y in range(2000, 2019):
            s1 = stats["eqratio_profit2_adding"]
            s2 = stats["eqratio_profit_adding"]
            s3= stats["eqratio_sales_adding"]
            stry = str(y)
            try:
                sy1 = s1[stry]
            except:
                sy1 = None

            try:
                sy2 = s2[stry]
            except:
                sy2 = None

            try:
                sy3 = s3[stry]
            except:
                sy3 = None

            self.parse(stry, (sy1, sy2, sy3), ys)
            continue

            print ""
            print sy1
            print sy2
            print sy3

        pass

    def parse(self, y, sylist, ys):
        (avggain, avgsy) = self.average(sylist)
        if avggain == None:
            return

        year = ys[y]
        match = 0
        goodmatch = 0
        for s in year:
            S = year[s]
            pe = S["eqratio_profit_adding"]
            se = S["eqratio_sales_adding"]
            g = S["gain"]
            if pe == None or se == None or g == None:
                continue
            if pe > avgsy and se > avgsy:
                match += 1
                if g > avggain:
                    goodmatch += 1

        if match > 0:
            print y, match, goodmatch, goodmatch*1.0/match

        pass

    def average(self, sylist):
        gain = 0
        syv = 0
        count = 0
        for sy in sylist:
            if sy == None:
                continue
            gain += sy[1]
            syv += sy[2]
            count += 1
        if count == 0:
            return (None, None)
        return (gain/count, syv/count)
 


class RelatedIndexes(BaseTestUnit):
    def cmd(self):
        return "index"

    def summary(self):
        return "parsing related indexes with gain"

    def run(self, args, opts):
        # study indexs from 1/23 to 5/2 every year
        if len(args) < 1:
            print "please specify the step"
            return

        if args[0] == "gen":
            iss = IndexStats( ((2000, 1, 1), (2018, 11, 30)), ((0, 1, 23), (0, 5, 7)), (GainIndex(), EQRatio("profit_adding"), EQRatio("profit2_adding"), EQRatio("sales_adding")))
#            iss = IndexStats( ((2016, 1, 1), (2018, 11, 30)), ((0, 1, 23), (0, 5, 7)), (GainIndex,PriceIndex))
            iss.run()
        elif args[0] == "parse":
            pi = ParseIndexes()
            pi.run()
        elif args[0] == "parse2":
            pi = Parse2Indexes()
            pi.run()
        pass
 

if __name__ == "__main__":
    ri = RelatedIndexes()






