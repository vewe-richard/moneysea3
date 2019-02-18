class BaseFilter:
    def run(self, S):       # return (True, None) or (False, "reason")
        return (True, None)
    def name(self):         # name of this filter
        return "basefilter"


# stock property caculate
class BaseProperty(BaseFilter):
    def run(self, S):       # return (True, property value) or (False, "reason")
        return (True, 0)

    def selectratio(self, ratio):    # the ratio we use to select stocks per this property
        return (0.5)


class ListFilters:
    def __init__(self, llfilters):
        self._llfilters = llfilters
        pass


    def run(self, liststocks):
        for S in liststocks:
            for ft in self._llfilters:
                rlt = ft.run(Stock)
                if not rlt[0]:
                    S.setfail(ft.name(), rlt[1])
                    self._fail.append(S)
                    break
                S.setval(ft.name(), rlt[1])
            if S in self._fail:
                continue
            self._pass.append(Stock)

# process list of stock property
class ListProperties(ListFilters):
    def stub(self):
        pass
