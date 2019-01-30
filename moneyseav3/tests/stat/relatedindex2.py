from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time
import json
from moneyseav3.tests.stat.indexes import *
from os import listdir
from os.path import isfile, join


class RelatedIndex2(BaseTestUnit):
    START_TIME = (0, 1, 25)
    HISTORY_DATA_INVEST_START = (2000, 1, 1)
    HISTORY_DATA_INVEST_END = (2018, 11, 30)
    INDEX_GOOD_RATIO = (1.0 / 3)
    GAIN_GOOD_RATIO = (1.0 / 2)

    RANGE_STEP = (2*30)  #two month
    INVEST_RANGE = (5*365) #5 years
    DEBUG = False

    OUTPUTDIR = "output/indexes/"
    OUTPUTDIR2 = "output/indexesstat/"

    def cmd(self):
        return "index2"

    def summary(self):
        return "parsing related indexes with gain"

    def run(self, args, opts):
        normal_idxs = (GainIndex(), PriceIndex(), MarketValueIndex(), PseYieldIndex())
        report_idxs = self.report_idxs()
        eqratio_idxs = self.eqratio_idxs()

        if self.DEBUG:
            self.HISTORY_DATA_INVEST_START = (2017, 1, 1)
            self.RANGE_STEP = (8*30)
            self.INVEST_RANGE = (16*30)
            self._ss = {"300230": Globals.get_instance().getstock("300230"), "002061": Globals.get_instance().getstock("002061"), "600276": Globals.get_instance().getstock("600276"),}
            self._indexes = (GainIndex(), EQRatio("profit_adding"), EQRatio("profit2_adding"), EQRatio("sales_adding"))

            aa = []
            aa.extend(normal_idxs)
            aa.extend(report_idxs)
            aa.extend(eqratio_idxs)
            self._indexes = aa
        else:
            self._ss = Globals.get_instance().stocks()
            aa = []
            aa.extend(normal_idxs)
            aa.extend(report_idxs)
            aa.extend(eqratio_idxs)
            self._indexes = aa


        if len(args) < 1:
            print "please specify the step"
            return

        if args[0] == "gen":
            for days in range(self.RANGE_STEP, self.INVEST_RANGE + self.RANGE_STEP, self.RANGE_STEP):
                self.everyrange(days)
        elif args[0] == "parse":
            self.parse()
        elif args[0] == "test":
            self.test()
        pass

    def everyrange(self, days):
        print "range(%d)"%(days, )
        hedt = datetime.date(self.HISTORY_DATA_INVEST_END[0], self.HISTORY_DATA_INVEST_END[1], self.HISTORY_DATA_INVEST_END[2])
        hedttime = time.mktime(hedt.timetuple())

        main = {}
        for y in range(self.HISTORY_DATA_INVEST_START[0], self.HISTORY_DATA_INVEST_END[0] + 1):
            print "\t", y
            # for every range
            sdt = datetime.date(y, self.START_TIME[1], self.START_TIME[2])
            sdttime = time.mktime(sdt.timetuple())
            edttime = sdttime + days * 3600 * 24
            edt = datetime.date.fromtimestamp(edttime)
            if edttime > hedttime:
                break
            
            ssi = {}
            for s in self._ss:
                ids = {}
                for idx in self._indexes:
                    idx.setup((sdt.year, sdt.month, sdt.day), (edt.year, edt.month, edt.day), self._ss[s], (sdt.year, 2))
                    ids[idx.name()] = idx.value()
                ssi[s] = ids

            main[y] = ssi
        path = self.OUTPUTDIR + str(days)
        json.dump(main, open(path,'w'))

    def report_idxs(self):
        reporttags = ("per_share_earnings", "per_share_asset", "per_share_cash2", "sales", 
            "msales_profit", "sales_profit", "invest_gain", "other_gain", 
            "total_profit", "profit", "profit2", "total_cash", "cach_adding", 
            "total_asset", "flow_asset", "total_debt", "flow_debt",
            "rights", "asset_yield", "profit_adding", "profit2_adding", "sales_adding")
        listidxs = []
        for tag in reporttags:
            listidxs.append(ReportIndex(tag))
        return listidxs

    def test(self):
        aa = self.report_idxs()
        aa.extend(self.eqratio_idxs())
        print aa
        pass

    def eqratio_idxs(self):
        return (EQRatio("profit_adding"), EQRatio("profit2_adding"), EQRatio("sales_adding"))

    def parse(self):
        mypath = "output/indexes/"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for f in onlyfiles:
            try:
                ys = json.load(open(join(mypath, f)))
            except Exception as e:
                print "skip", f
                print e
                continue
            if len(ys.keys()) < 1:
                print "keys lengh is zero"
                continue

            main = {}
            for y in ys:
                main[y] = self.parseyear(y, ys[y])
                self.statistic(main[y], y, ys[y])
            self.statoutput(f, main)

    def parseyear(self, year, ydata):
        ystat = {}
        for s in ydata:
            keys = ydata[s]
            break

        for k in keys:
            ystat[k] = {"baseline":self.parseindex(k, ydata),}

        return ystat

    def parseindex(self, key, ydata):
#        print "---"
        ll = []
        for s in ydata:
            if ydata[s][key] == None:
                continue
            ll.append(ydata[s][key])
        sll = sorted(ll)
        l = len(sll)
        if l == 0:
            return None

        if key == "gain":
            offset = int(l * self.GAIN_GOOD_RATIO)
        else:
            offset = int(l * self.INDEX_GOOD_RATIO)

        baseline = sll[offset]
#        print key, sll
#        print "offset:", offset, baseline

#        print "+++"
        return baseline

    def statistic(self, baseline, year, ydata):
        bbs = baseline["gain"]["baseline"]
        if bbs == None:
            return None

        for k in baseline:
            baseline[k]["goodindex"] = 0
            baseline[k]["goodgain"] = 0


        for s in ydata:
            S = ydata[s]
            sgain = S["gain"]
            if sgain == None:
                continue

            for k in S:
                if k == "gain":
                    continue
                kbs = baseline[k]["baseline"]
                if kbs == None:
                    continue
                if S[k] == None:
                    continue

#                print k, S[k], kbs, bbs
                if S[k] > kbs:
                    baseline[k]["goodindex"] += 1
                    if S["gain"] > bbs:
                        baseline[k]["goodgain"] += 1

    def statoutput(self, f, main):
        for y in main:
            keys = main[y].keys()
            break
        summ = {}
        for k in keys:
            summ[k] = {"goodindex":0, "goodgain":0}
        for y in main:
            for k in main[y]:
                summ[k]["goodindex"] += main[y][k]["goodindex"]
                summ[k]["goodgain"] += main[y][k]["goodgain"]
        for k in summ:
            if summ[k]["goodindex"] == 0:
                summ[k]["ratio"] = 0.00001
                continue
            summ[k]["ratio"] = summ[k]["goodgain"] * 1.0 / summ[k]["goodindex"]

        path = self.OUTPUTDIR2 + f
        json.dump(summ, open(path,'w'))

        pass










