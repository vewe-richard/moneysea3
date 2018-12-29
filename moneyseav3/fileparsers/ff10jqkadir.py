from moneyseav3.fileparsers.baseparser import BaseParser
from os import listdir

class FF10jqkaDir(BaseParser):
    def doparse(self):
        self._stocks = {}
        for f in listdir(self._filepath):
            items = f.split("-")
            if len(items) != 2:
                continue
            self._stocks[items[1]] = items[0]
        pass

    def allstocks(self):           #a dict, key is the stockid, content is the pinyin
        return self._stocks
