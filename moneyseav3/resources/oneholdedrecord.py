from moneyseav3.fileparsers.oneholdedrecordfile import OneHoldedRecordFile

class OneHoldedRecord:
    def __init__(self, recordpath):
        self._recordpath = recordpath
        self._hsf = OneHoldedRecordFile(recordpath)
        self._hsf.doparse()
        pass
    def date(self):
        items = self._recordpath.split("-")
        return items[1]
    def time(self):
        items = self._recordpath.split("-")
        return items[2]
    def stocks(self):      
        return self._hsf.stocks()
    def getstock(self, idx):  #return (total, buy)
        return self._hsf.stocks()[idx]
    def gettotal(self, idx):
        return float(self._hsf.stocks()[idx][OneHoldedRecordFile.STOCKS_TOTAL_VALUE])
    def getprice(self, idx):
        return float(self._hsf.stocks()[idx][OneHoldedRecordFile.STOCKS_PRICE])
    def gettotalholded(self, idx):
        return float(self._hsf.stocks()[idx][OneHoldedRecordFile.STOCKS_HOLDED])

if __name__ == "__main__":
    ohr = OneHoldedRecord("input/holded/holded-20181120-1330")
    print ohr.date()
    print ohr.time()
    print ohr.stocks()
    print ohr.getstock("601998")
    print ohr.gettotal("601998")
    print ohr.getprice("601998")
    print ohr.gettotalholded("601998")
