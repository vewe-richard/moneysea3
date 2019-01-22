from moneyseav3.globals import Globals
from moneyseav3.tests.basetestunit import BaseTestUnit
from moneyseav3.resources.fadata import FaData

class FadataTest(BaseTestUnit):
    def cmd(self):
        return "fadata"

    def summary(self):
        return "Test Fadata"

    def run(self, args, opts):
        self._totalsample = 0
        self._mismatchsample = 0
        self.test1()
        self.test2()
        self.test3()
        self.test4()


    def test1(self):
        fd1 = FaData("300230", source=FaData.NETEASE)
        r1 = fd1.report(2017, 3)

        fd2 = FaData("300230", source=FaData.TONGHS)
        r2 = fd2.report(2017, 3)

        self._samekey = []
        self._diffkey = []
        for k in r2.keys():
            if k in r1.keys():
                self._samekey.append(k)
            else:
                self._diffkey.append(k)
#        print self._samekey
#        print self._diffkey
        for k in self._samekey:
            if r1[k] == None or r2[k] == None:
                continue
            delta = (r2[k] - r1[k])/r1[k]
            print "key ", k, ",\t delta: ", delta
            if abs(delta) > 0.01:
                raise(Exception("not match"))

        print "netease: \t",  fd1.oldest(), "---", fd1.latest()
        print "TongHS: \t",  fd1.oldest(), "---",  fd1.latest()

        print "Test 1 Pass\n"
        pass

    def test2(self):
        cmplist = ['profit2_adding', 'profit_adding', 'sales_adding']

        fd1 = FaData("300230", source=FaData.NETEASE)
        r1 = fd1.report(2017, 3)

        fd2 = FaData("300230", source=FaData.TONGHS)
        r2 = fd2.report(2017, 3)

        for k in cmplist:
            print r1[k]
            print r2[k]

        print "Test 2 Pass\n"
        pass

    def test3(self):
        self.compare("300230", "profit_adding")
        print "Test 3 Pass\n"
        pass


    def compare(self, stockid, tag):
        fd1 = FaData(stockid, source=FaData.NETEASE)
        fd2 = FaData(stockid, source=FaData.TONGHS)
        for y in range(2009, 2018):
            for s in range(0, 4):
                r1 = fd1.report(y, s)
                r2 = fd2.report(y, s)
                if r1 == None or r2 == None:
                    continue
                try:
                    p1 = r1[tag]
                    p2 = r2[tag]
                    delta = abs(p1 - p2)
                    ratio = abs((p1 - p2)/p2)
                    self._totalsample += 1

                    if delta < 40:
                        continue

                    if ratio < 0.3:
                        continue

                    print stockid, "(", y, s, ")", "[", p1, p2, "]", "delta/ratio is big", delta, ratio
                    self._mismatchsample += 1
                except Exception as e:
                    pass

    def test4(self):
        self._totalsample = 0
        self._mismatchsample = 0

        ss = Globals.get_instance().getff10jqka().allstocks()
        count = 0
        for s in ss:
            self.compare(s, "sales_adding")
            count += 1
#            if count > 10:
#                break

        ratio = (self._mismatchsample * 1.0 / self._totalsample)
        print "mismatch ratio: ", ratio
        if abs(ratio) < 0.06:
            print "Test 4 Pass\n"


        pass
 










