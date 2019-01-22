# coding=utf-8
# file source: On Ubuntu, using chromium to open 同花顺--永利股份，select 财务指标，按报告期
# Provide: 
# Verify: every season, 净资产收益率-摊薄 = 每股收益/每股净资产

from moneyseav3.fileparsers.ffbase import FFBase

class FF10jqka(FFBase):
    def doparse(self):
        #build datalist for parsing
        datalist = list()
        with open(self._filepath) as f:
            for line in f:
                items = line.split()
                if len(items) < 8:
                    continue
                datalist.append(items)

        i = 0
        self._oldest = 100000
        self._latest = -10000

        if len(datalist) < 1:
            return
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
        pass



    TABLE = ("per_share_earnings", "profit", "profit_adding", "profit2", "profit2_adding",
            "sales", "sales_adding", "per_share_asset", "asset_yield", "asset_yield2", 
            "asset_debt_ratio", "per_share_fund", "per_share_keep_profit", "per_share_cash",
            "sales_gross")
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
            except:
                fd[key] = None
            index += 1

        return fd


if __name__ == "__main__":
    ff = FF10jqka("input/stocks/ff10jqka/ylgf-300230/finance")
#    ff = FF10jqka("input/stocks/yxkj-300231/finance")
    ff.doparse()
#    print ff.allreports()
#    print ff.oldestreport()
#    print ff.latestreport()
#    print ff.yearreport(2017)
    print ff.report(2011, 2)
    pass

