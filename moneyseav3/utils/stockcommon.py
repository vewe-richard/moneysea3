class StockCommon:
    def stockidsimple(self, stockid):
        if stockid[0] == 's':
            val = stockid[2:]
        else:
            val = stockid
        try:
            int(val)
            return val
        except:
            return None

    def stockidlocation(self, stockid):
        if stockid[0] == "6":
            return "sh" + stockid
        else:
            return "sz" + stockid
        return


if __name__ == "__main__":
    pass
