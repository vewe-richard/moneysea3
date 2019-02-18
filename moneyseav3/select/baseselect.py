


# 以props排序，找出它们的前部交集
# prefilters, props and postfilters are all list of objects of BaseFilter
#
class BaseSelect:
    def __init__(self, prefilters, props, postfilters):
        self._prefilters = prefilters
        self._props = props
        self._postfilters = postfilters
        pass

    def run(self):
        print "goo"
'''
run:
    ass = Types.stocks() or Globals.liststocks()

    prelf = ListFilters(prefilters)
    prelf.run(ass)
    pass = prelf.pass()

    lp = ListProperties(props)
    lp.run(pass)
    pass2 = lp.pass()
            
    #sort
    ads = dict()
    for every prop
        ll = ads[prop.name()] = []
        for every Stock in pass2
            if len(ll) == 0:
                ll.append(Stock)
            else:
                for every Stock in ll as iStock
                    if Stock.getval(prop.name()) > iStock.getval(prop.name()):
                        ll.insert()
                    else:
                        ll.append(Stock)
                
. intersections
    for every prop
        end = len(ads[prop.name()]) * prop.selectratio()
        half_ads[prop.name()] = ads[prop.name()][0:end]

    first = half_ads[first prop name()]
    copy all Stocks in first to overlap

    for s in first:
        for every prop:
            if not s in half_ads[prop name]
                overlap.remove(s)
                break

. post filters
    Using ListFilters()
'''



if __name__ == "__main__":
    bs = BaseSelect(None, None, None)
    bs.run()
