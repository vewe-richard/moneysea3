# coding=utf-8
from moneyseav3.fileparsers.baseparser import BaseParser
import datetime

#financial data are stored in self._data{}
# _data[0] _data[1] _data[2] _data[3] --- 2009 first, second, third, forth season report data
# _data[4] _data[5] _data[6] _data[7] --- 2010 first, second, third, forth season report data
class FFBase(BaseParser):
    MAX_YEARS = 22  #max years of data to save for parsing

    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)

        now = datetime.datetime.now()

        #[self._start, self._end]
        self._start = now.year - self.MAX_YEARS + 1 #start year
        self._end = now.year                        #end year

        self._data = {}
        for i in range(self.MAX_YEARS * 4):
            self._data[i] = None

        self._oldest = 100000
        self._latest = -10000
        pass

    def getindex(self, year, season):
        if year > self._end:
            return -1
        if year < self._start:
            return -1
        if season < 0:
            return -1
        if season > 3:
            return -1
        index = (year - self._start)*4 + season
        return index

    def yearreport(self, year):
        index = self.getindex(year, 3)
        return self._data[index]

    def report(self, year, season):
        index = self.getindex(year, season)
        if index == -1:
            return None
        return self._data[index]

    def range(self):
        return (self._oldest, self._latest)

    def latestreport(self):
        return self._data[self._latest]

    def oldestreport(self):
        return self._data[self._oldest]

    def oldestindex(self):
        return self._oldest

    def latestindex(self):
        return self._latest

    def allreports(self):
        return self._data

    #   protected
    def year_season(self, date):
        try:
            items = date.split("-")
            year = int(items[0])
            month = int(items[1])
            if month > 0 and month < 4:
                season = 0
            elif month > 3 and month < 7:
                season = 1
            elif month > 6 and month < 10:
                season = 2
            elif month > 9 and month < 13:
                season = 3
            else:
                season = -1
            return (year, season)
        except:
            return (-1,-1)

    def parseadding(self, text):
        ret = text.replace("%", "")
        return float(ret)

    def parsemoney(self, text):
        ret = 0
        if "亿" in text:
            ret = float(text.replace("亿", "").strip()) * 10000 * 10000
        elif "万" in text:
            ret = float(text.replace("万", "").strip()) * 10000
        else:
            ret = float(text.strip())
        return ret
