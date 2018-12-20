# coding=utf-8

from moneyseav3.fileparsers.baseparser import BaseParser
from moneyseav3.config import Config

class StockIdNameMapFile(BaseParser):
    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)
        self._map = {}
        pass

    def doparse(self):
        with open(self._filepath) as f:
            for line in f:
                for i in line.split(")"):
                    items = i.split("(")
                    if len(items) != 2:
                        continue
                    self._map[items[1].strip()] = items[0].strip()
        pass

    def getmap(self):
        return self._map


if __name__ == "__main__":
    smf = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_SHA)
    smf.doparse()
    print smf._map["600505"]
    pass
