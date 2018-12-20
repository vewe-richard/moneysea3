
from moneyseav3.config import Config
from moneyseav3.fileparsers.stockidnamemapfile import StockIdNameMapFile

class StockIdNameMapping:
    def __init__(self):
        sha = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_SHA)
        sha.doparse()
        sz = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_SZ)
        sz.doparse()
        op = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_OPEN)
        op.doparse()
        self._map = dict(sha._map.items() + sz._map.items() + op._map.items())
        pass

    def getname(self, sid):
        name = None
        try:
            name = self._map[sid]
        except:
            name = "--"
        return name

    def getmap(self):
        return self._map


if __name__ == "__main__":
    sin = StockIdNameMapping()
    print sin.getname("600004")
    pass
