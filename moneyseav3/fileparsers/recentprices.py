
from os import listdir
from moneyseav3.config import Config

class RecentPrices:
    def listpricefiles(self):
        mylist = []
        for f in listdir(Config.PRICES_PATH):
            if len(f.split("-")) != 2:
                continue
            mylist.append(f)
        mylist.sort()
        return mylist


if __name__ == "__main__":
    rp = RecentPrices()
    print rp.listpricefiles()
