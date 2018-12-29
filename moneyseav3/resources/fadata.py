from moneyseav3.globals import Globals

class FaData:
    def __init__(self, stockid, source = None):        # consturct from FFNetease, if not suitable, consturct from 10jqka
        pass

    def yearreport(self, year): # return dict
        pass

    def report(self, year, season):
        pass

    def latest(self):         # (year, season)
        pass

    def oldest(self):         # (year, season)
        pass

    def all(self):            # list of all valid reports
        pass

    def latestreport(self):   # latest report
        pass

    def oldestreport(self):   # oldest report
        pass
 

if __name__ == "__main__":

    gbls = Globals.get_instance()
    ff10 = gbls.getff10jqka()
    print ff10.allstocks()
