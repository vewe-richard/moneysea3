# coding=utf-8
# file source: On Ubuntu, using chromium to open 招商证券, login in and select 资金股份(CTRL+A), copy and paste to vim
# Provide: 总资产，市值，余额；每只股票和它对应的信息
# Verify: 总资产应该等于市值加余额; 其中每只股票的市值和等于总市值


from moneyseav3.fileparsers.baseparser import BaseParser

class OneHoldedRecordFile(BaseParser):
    STOCKS_HOLDED = 0
    STOCKS_FREE = 1
    STOCKS_PRICE = 2
    STOCKS_BUY_PRICE = 3
    STOCKS_TOTAL_VALUE = 4

    def doparse(self):
        self.holded = {}
        with open(self._filepath) as f:
            prev_not_null_line = None
            for line in f:
                if "总资产（元）" in line:
                    self.total =  float(prev_not_null_line.strip().replace(",", ""))
                elif "市值（元）" in line:
                    self.market = float(prev_not_null_line.strip().replace(",", ""))
                elif "可用（元）" in line:
                    self.cash = float(prev_not_null_line.strip().replace(",", ""))
                elif "人民币" in line:
                    self.addstock(line)

                if len(line.strip()) > 1:
                    prev_not_null_line = line

        if not self.verify():
            raise ValueError("file parser verifying failed")

    def verify(self):
        if abs(self.total - self.market - self.cash) > 300:
           return False
        total = 0
        for stock in self.holded:
            total += float(self.holded[stock][self.STOCKS_TOTAL_VALUE].strip())
        if abs(self.market - total) > 200:
            return False
        return True

    def addstock(self, line):
        items = line.strip().split()
        if len(items) < 12:
            return
        self.holded[items[0]] = items[2:7]

    def stocks(self):
        return self.holded

if __name__ == "__main__":
    hsf = OneHoldedRecordFile("input/holded/holded-20181120-1330")
    hsf.doparse()
    print hsf.stocks()
    pass
