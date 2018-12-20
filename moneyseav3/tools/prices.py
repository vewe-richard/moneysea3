import json
import urllib2
import datetime
from moneyseav3.globals import Globals
from moneyseav3.utils.stockcommon import StockCommon
from moneyseav3.config import Config

class Prices:
    def run(self):
        allstocks = Globals.get_instance().stocks().keys()

        count = 0
        mylist = ""
        self.plist = {}
        for item in allstocks:
            mylist += StockCommon().stockidlocation(item) + ","
            count += 1
            if count == 3:
                self.request(mylist)
                count = 0
                mylist = ""
        if count > 0:
            self.request(mylist)
        n = datetime.datetime.now()
        name = Config.PRICES_PATH + "/%04d%02d%02d-%02d%02d"%(n.year, n.month, n.day, n.hour, n.minute)
        json.dump(self.plist, open(name,'w'))

    def request(self, mylist):
        myurl='http://hq.sinajs.cn/list=' + mylist
        req = urllib2.Request(url = myurl)
        res = urllib2.urlopen(req)
        res = res.read()
        lines = res.split("\n")
        for line in lines:
            vals = line.split(",")
            if len(vals) < 2:
                continue
            if len(vals) < 20:
                print line
                print "Unknown response on " + mylist
                continue
            idx = vals[0][13:19]
            price = float(vals[2])
            self.plist[idx] = price
