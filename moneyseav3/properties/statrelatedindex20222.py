
from moneyseav3.properties.baseproperties import *
from moneyseav3.tests.stat.indexes import *

class Settings:
    PLAN_BUY_DATE = (2019, 2, 22)
    REPORT_SEASON = (-1, 2)
    REF_PRICE_DATE = (2019, 2, 18)

class EQRA_Prop(BaseProperty):
    def __init__(self, tag, rg):
        self._tag = tag
        self._range = rg
        pass

    def run(self, S):       # return (True, property value) or (False, "reason")
        eqra = EQRangeAdding(self._tag, self._range, Settings.REF_PRICE_DATE)
        eqra.setup(Settings.PLAN_BUY_DATE, None, S, reportseason = Settings.REPORT_SEASON)
        if eqra.value() == None:
            return (False, "fail")
        return (True, eqra.value())

    def name(self):         # name of this filter
        return "eqra_" + self._tag + str(self._range)

    def selectratio(self, ratio):    # the ratio we use to select stocks per this property
        return (0.5)


class EQPA_Prop(BaseProperty):
    def __init__(self, tag, rg):
        self._tag = tag
        self._range = rg
        pass

    def run(self, S):       # return (True, property value) or (False, "reason")
        eqpa = EQPrevAdding(self._tag, self._range, Settings.REF_PRICE_DATE)
        eqpa.setup(Settings.PLAN_BUY_DATE, None, S, reportseason = Settings.REPORT_SEASON)
        if eqpa.value() == None:
            return (False, "fail")
        return (True, eqpa.value())

    def name(self):         # name of this filter
        return "eqpa_" + self._tag + str(self._range)

    def selectratio(self, ratio):    # the ratio we use to select stocks per this property
        return (0.5)


if __name__ == "__main__":
    from moneyseav3.globals import Globals

    s = Globals.get_instance().getstock("300230")

    eqrap = EQRA_Prop("profit", -1)
    print eqrap.name()
    print eqrap.run(s)

    print "---"

    eqpap = EQPA_Prop("profit", -1)
    print eqpap.name()
    print eqpap.run(s)
 

    pass
