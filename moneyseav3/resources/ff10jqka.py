from moneyseav3.config import Config
from moneyseav3.fileparsers.ff10jqkadir import FF10jqkaDir

class FF10jqka:
    def __init__(self):
        self._dir = FF10jqkaDir(Config.STOCKS_PATH_THS)
        self._dir.doparse()
        pass

    def allstocks(self):                #a dict, key is the stockid, content is the pinyin
        return self._dir.allstocks()

    def getpath(self, stockid):               #return path of the stock
        return Config.STOCKS_PATH_THS + "/" + self._dir.allstocks()[stockid] + "-" + stockid

    def getpinyin(self, stockid):
        return self._dir.allstocks()[stockid]

    def getids(self, pinyin):
        all = self._dir.allstocks()
        ids = []
        for a in all:
            if all[a] == pinyin:
                ids.append(a)
        return ids


if __name__ == "__main__":
    iss = FF10jqka()
    print iss.allstocks()
    
