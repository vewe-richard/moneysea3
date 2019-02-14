from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
import datetime, time
import json
from moneyseav3.tests.stat.indexes import *
from os import listdir
from os.path import isfile, join
import sys


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
    OUTPUTDIR3 = "output/mixstat/"
    OUTPUTDIR4 = "output/automixstat/"

    def cmd(self):
        return "index2"

    def summary(self):
        return "parsing related indexes with gain"

    def run(self, args, opts):
        normal_idxs = (GainIndex(), PriceIndex(), MarketValueIndex(), PseYieldIndex(), PriceDeltaIndex())
        report_idxs = self.report_idxs()
        eqratio_idxs = self.eqratio_idxs()
        rangeadding_idxs = self.rangeadding_idxs()

        if self.DEBUG:
            self.HISTORY_DATA_INVEST_START = (2017, 1, 1)
            self.RANGE_STEP = (8*30)
            self.INVEST_RANGE = (16*30)
            self._ss = {"300230": Globals.get_instance().getstock("300230"), "002061": Globals.get_instance().getstock("002061"), "600276": Globals.get_instance().getstock("600276"),"600518": Globals.get_instance().getstock("600518"),
                    "600801": Globals.get_instance().getstock("600801"),"600585": Globals.get_instance().getstock("600585"),}
            self._indexes = (GainIndex(), EQRatio("profit_adding"), EQRatio("profit2_adding"), EQRatio("sales_adding"))

            aa = []
            aa.extend(normal_idxs)
#            aa.extend(report_idxs)
#            aa.extend(eqratio_idxs)
            self._indexes = aa
        else:
            self._ss = Globals.get_instance().stocks()
            aa = []
            aa.extend(normal_idxs)
            aa.extend(report_idxs)
            aa.extend(eqratio_idxs)
            aa.extend(rangeadding_idxs)
            self._indexes = aa


        if len(args) < 1:
            print "please specify the step"
            return

        self._automix = None
        if args[0] == "gen":
            for days in range(self.RANGE_STEP, self.INVEST_RANGE + self.RANGE_STEP, self.RANGE_STEP):
                self.everyrange(days)
        elif args[0] == "parse":
            self.parse(self.statistic, self.OUTPUTDIR2)
        elif args[0] == "output":
            self.output("output/indexesstat/")
        elif args[0] == "outputmix":
            self.output("output/mixstat/")
        elif args[0] == "test":
            self.test()
        elif args[0] == "mixparse":
            self.parse(self.mixstatistic, self.OUTPUTDIR3)
        elif args[0] == "automixparse":
            self.parse(self.automixstatistic, self.OUTPUTDIR4)
        elif args[0] == "outputautomix":
            self.outputautomix()
        pass

    def automixindexes(self):
        return ( 'eqratio_profit_adding', 'report.profit_adding_2', 'eqratio_profit2_adding', 'ra_profit_-1', 'eqratio_sales_adding', 'ra_profit_-2', 'ra_profit2_-1', 'report.profit2_adding_2', 'ra_per_share_earnings_-1')

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
#        aa = self.report_idxs()
#        aa.extend(self.eqratio_idxs())
        aa = self.rangeadding_idxs()
        print aa
        pass

    def eqratio_idxs(self):
        return (EQRatio("profit_adding"), EQRatio("profit2_adding"), EQRatio("sales_adding"))

    def rangeadding_idxs(self):
        ll = []
        for rg in range(-6, 0):
            if rg == 0:
                continue
            for tag in ("profit", "profit2", "sales", "per_share_earnings"):
                ra = RangeAdding(tag, rg)
                ll.append(ra)
        return ll

    def parse(self, statmethod, outdir):
        mypath = "output/indexes/"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for f in onlyfiles:
#            f = "1860"
            print "parse file", f
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
                print "\tparse baseline for ", y
                main[y] = self.parseyear(y, ys[y])
                print "\tcaculate the stat for ", y
                statmethod(main[y], y, ys[y])
            print "output for", f
            self.statoutput(f, main, outdir)
#            break


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
        sll = sorted(ll, reverse = True)
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

#    MIXINDEXES = ( ("ra_sales_5",), ('ra_sales_4', 'ra_sales_5', 'ra_profit_4', 'ra_profit_5', 'ra_profit2_4', 'ra_profit_3', 'ra_profit2_5','ra_sales_3','ra_profit2_3', 'ra_profit_2','ra_sales_2', 'ra_profit2_2',))
    MIXINDEXES = ( ('eqratio_profit_adding', 'report.profit_adding_2', 'eqratio_profit2_adding', 'ra_profit_-1', 'eqratio_sales_adding', 'ra_profit_-2', 'ra_profit2_-1', 'report.profit2_adding_2'),
            ('eqratio_profit2_adding', 'eqratio_profit_adding', 'ra_profit_-1', 'report.profit_adding_2', 'eqratio_sales_adding', 'ra_profit2_-1', 'ra_profit_-2', 'ra_per_share_earnings_-1', ))



    def mixstatistic(self, baseline, year, ydata):
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

            for mi in self.MIXINDEXES:
                valuable = True
                good = True
                for k in mi:
                    kbs = baseline[k]["baseline"]
                    if kbs == None:
                        valuable = False
                        break
                    if S[k] == None:
                        valuable = False
                        break
                    if S[k] < kbs:
                        good = False
                        break
                if not valuable:
                    continue
                if good:
                    baseline[mi[0]]["goodindex"] += 1
                    if S["gain"] > bbs:
                        baseline[mi[0]]["goodgain"] += 1


    def statoutput(self, f, main, outdir):
        for y in main:
            keys = main[y].keys()
            break
        summ = {}
        for k in keys:
            summ[k] = {"goodindex":0, "goodgain":0}
        for y in main:
            for k in main[y]:
                if k == "gain":
                    continue
                try:
                    summ[k]["goodindex"] += main[y][k]["goodindex"]
                    summ[k]["goodgain"] += main[y][k]["goodgain"]
                except:
                    pass
        for k in summ:
            if summ[k]["goodindex"] == 0:
                summ[k]["ratio"] = 0.00001
                continue
            summ[k]["ratio"] = summ[k]["goodgain"] * 1.0 / summ[k]["goodindex"]

        path = outdir + f
        json.dump(summ, open(path,'w'))

        pass

    def output(self, mypath):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for f in onlyfiles:
            try:
                stat = json.load(open(join(mypath, f)))
            except Exception as e:
                print "skip", f
                print e
                continue
            if len(stat.keys()) < 1:
                print "keys lengh is zero"
                continue
            self.outputrange(f, stat)

        pass

    def outputrange(self, f, stat):
        ll = []
        for k in stat:
            ll.append((k, stat[k]["ratio"]))
        sl = sorted(ll, key=lambda x: x[1], reverse = True)
        print "range:", f
        count = 0
        for i in sl:
            if i[1] < 0.001:
                continue
            if int(i[1]*10) == 5 or int(i[1]*10) == 4:
#                continue
                pass

            print i
            count += 1
            if count > 30:
#                break
                pass


    def automixstatistic(self, baseline, year, ydata):
        if self._automix == None:
            print "generate auto mix indexes"
            self._automix = self.genautomix(baseline)

        bbs = baseline["gain"]["baseline"]
        if bbs == None:
            return None

        for k in self._automix:
            try:
                baseline[k]["goodindex"] = 0
                baseline[k]["goodgain"] = 0
            except:
                baseline[k] = {}
                baseline[k] = {}
                baseline[k]["goodindex"] = 0
                baseline[k]["goodgain"] = 0

#        print baseline
#        print ""

        for s in ydata:
            S = ydata[s]
            sgain = S["gain"]
            if sgain == None:
                continue

            for mi in self._automix:
                valuable = True
                good = True
                ll = self._automix[mi]

                for k in ll:
                    kbs = baseline[k]["baseline"]
                    if kbs == None:
                        valuable = False
                        break
                    if S[k] == None:
                        valuable = False
                        break
                    if S[k] < kbs:
                        good = False
                        break
                if not valuable:
                    continue
                if good:
                    baseline[mi]["goodindex"] += 1
                    if S["gain"] > bbs:
                        baseline[mi]["goodgain"] += 1


    def genautomix(self, baseline):
        automix = {}
        v = []
        for k in self.automixindexes(): # baseline:
            if k == "gain":
                continue
            v.append([k,])
            automix[k] = [k,]

        for k in self.automixindexes(): #baseline:
            if k == "gain":
                continue
            nextv = []
            for kk in self.automixindexes(): #baseline:
                if kk == "gain":
                    continue
                for pkk in v:
                    if kk in pkk:
                        continue
                    tmp = []
                    tmp.extend(pkk)
                    tmp.append(kk)
                    if self.repeated(nextv, tmp):
                        continue
                    nextv.append(tmp)
                    name = self.name(tmp)
                    automix[name] = tmp
            v = nextv
        return automix

    def repeated(self, parent, item):
        for a in parent:
            #if a is same as item
            same = True
            for i in item:
                if i in a:
                    continue
                same = False
                break
            if same:
                return True
        return False


    def name(self, ll):
        strr = ""
        for i in ll:
            strr += i
            strr += "-"
        return strr


    def outputautomix(self):
        onlyfiles = [f for f in listdir(self.OUTPUTDIR4) if isfile(join(self.OUTPUTDIR4, f))]
        
        ll = []
        for f in onlyfiles:
            try:
                stat = json.load(open(join(self.OUTPUTDIR4, f)))
            except Exception as e:
                print "skip", f
                print e
                continue
            for item in stat:
                ll.append((stat[item]["ratio"], f + "#" + item, stat[item]["goodgain"], stat[item]["goodindex"]))

        sll = sorted(ll, key=lambda x: x[0])  
        for i in sll:
            print i
        pass








