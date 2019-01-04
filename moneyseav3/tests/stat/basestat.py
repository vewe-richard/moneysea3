import datetime, time

class BaseStat:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def price(self, date):
        return 1.0

    def addings(self):

        try:
            startdate = datetime.date(self._start[0], self._start[1], self._start[2])
        except:
            return None

        startp = self.price(self._start)
        tmptime = time.mktime(startdate.timetuple())
        endstr = "%04d-%02d-%02d"%(self._end[0], self._end[1], self._end[2])
        al = []
        adding = 0
        while True:
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break

            refp = self.price((dt.year, dt.month, dt.day))
            if refp != None:
                adding = (refp - startp)/startp

            al.append(adding)
            tmptime += (3600*24)
        return al

    def prices(self):
        try:
            startdate = datetime.date(self._start[0], self._start[1], self._start[2])
        except:
            return None

        tmptime = time.mktime(startdate.timetuple())
        endstr = "%04d-%02d-%02d"%(self._end[0], self._end[1], self._end[2])

        pl = []
        prevp = 0
        while True:
            dt = datetime.date.fromtimestamp(tmptime)
            if str(dt) > endstr:
                break

            p = self.price((dt.year, dt.month, dt.day))
            if p == None or p < 0.1:
                p = prevp
            pl.append(p)
            prevp = p
            tmptime += (3600*24)
        return pl




