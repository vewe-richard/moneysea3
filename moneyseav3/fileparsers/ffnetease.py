from moneyseav3.fileparsers.ffbase import FFBase
import sys

class FFNetEase(FFBase):
    def doparse(self):
        #build datalist for parsing
        datalist = list()
        with open(self._filepath) as f:
            for line in f:
                items = line.split(",")
                if len(items) < 8:
                    continue
                datalist.append(items)

        if len(datalist) < 1:
            return

        i = 0
        self._oldest = 100000
        self._latest = -10000


        for date in datalist[0]:
            year, season = self.year_season(date)
            index = self.getindex(year, season)
            if index == -1:
                i += 1
                continue

            d = self.constructdata(year, season, datalist, i)

            self._data[index] = d

            if index > self._latest:
                self._latest = index
            if index < self._oldest:
                self._oldest = index
            i += 1

        for index in range(self._oldest + 4, self._latest + 1):
            fd = self._data[index]
            if fd == None:
                continue
            pfd = self._data[index - 4]
            if pfd == None:
                continue

            fd["profit_adding"] = self.adding(pfd, fd, "profit")
            fd["profit2_adding"] = self.adding(pfd, fd, "profit2")
            fd["sales_adding"] = self.adding(pfd, fd, "sales")
        pass

    def adding(self, pfd, fd, tag):
        if pfd[tag] == None or fd[tag] == None:
            return None
#        if pfd[tag] < 1000000:
#            return 999999
        if abs(pfd[tag]) < 1:
            return None

        if abs(fd[tag]) < 1:
            return None

        ratio = (fd[tag] - pfd[tag])/abs(pfd[tag])
        return ratio * 100


    TABLE = ("per_share_earnings", "per_share_asset", "per_share_cash2", "sales", 
            "msales_profit", "sales_profit", "invest_gain", "other_gain", 
            "total_profit", "profit", "profit2", "total_cash", "cach_adding", 
            "total_asset", "flow_asset", "total_debt", "flow_debt",
            "rights", "asset_yield")
    def constructdata(self, year, season, datalist, i):
        fd = {}
        fd["year"] = year
        fd["season"] = season

        index = 1
        for key in self.TABLE:
            try:
                cnt = datalist[index][i]
                if "%" in cnt:
                    fd[key] = self.parseadding(cnt)
                else:
                    fd[key] = self.parsemoney(cnt)
                if index > 2 and index < 18:
                    fd[key] *= 10000
            except:
                fd[key] = None
            index += 1
        return fd


if __name__ == "__main__":
    ff = FFNetEase("input/stocks/netease/zycwzb_002495.html?type=report")
    ff.doparse()
#    print ff.allreports()
    print ff.report(2011, 2)
