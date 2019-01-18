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
#

from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time

class IndexStats:
    DEBUG = True

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
            start = (year, self._rstart[1], self._rstart[2])
            end = (year, self._rend[1], self._rend[2])
            #for every stock
            ss = Globals.get_instance().stocks()
            count2 = 0
            thisyear = {}
            for s in ss:
                S = ss[s]
                ids = {}
                for index in self._indexs:
                    idx = index()
                    idx.setup(start, end, S)
                    ids[idx.name()] = idx.value()
                thisyear[s] = ids
                count2 += 1
                if count2 > 3 and self.DEBUG:
                    break
            years[year] = thisyear
            count += 1
            if count > 2 and self.DEBUG:
                break
        print years
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
        hps = self._s.historypricesshare(self._start)
        print hps
        return 0

class RelatedIndexes(BaseTestUnit):
    def cmd(self):
        return "index"

    def summary(self):
        return "parsing related indexes with gain"

    def run(self, args, opts):
        # study indexs from 1/23 to 5/2 every year
#        iss = IndexStats( ((2000, 1, 1), (2018, 11, 30)), ((0, 1, 23), (0, 5, 2)), (GainIndex,))
        iss = IndexStats( ((2016, 1, 1), (2018, 11, 30)), ((0, 1, 23), (0, 5, 2)), (GainIndex,))
        iss.run()
        pass
 

if __name__ == "__main__":
    ri = RelatedIndexes()






