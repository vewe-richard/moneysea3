
from moneysea.actions.baseaction import BaseAction
from moneysea.globals import Globals
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter
from moneysea.addings.defaultadding import DefaultAdding

class ParseAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "parse"

    def summary(self):
        return "parse one stock"


    def description(self):
        return '''
SYNOPSIS: 
    [--finance] parse <pinyin | id>
DESCRIPTIONS:
    parse the specific stock, show parsing result

OPTIONS:
    <pinyin | id>
        pinyin or stock id
    --finance
        only show finance information
'''


    def run(self, args, opts):
        if len(args) < 1:
            print "Please specific the stock in id or pinyin"
            return

        try:
            int(args[0])
            idx = args[0]
        except:
            #it is pinyin
            ids = Globals.get_instance().getinputstocks().getids(args[0])
            if len(ids) == 1:
                idx = ids[0]
            elif len(ids) > 1:
                idx = self.select(ids)
            else:
                print "Please specific a correct stock"
                return

        stock = Stock(idx, DefaultAdding(idx))

        print stock.id()
        print stock.name()
        print stock.types()
        print "industry:", stock.industry()
        print stock.n(), stock.p()

        if not stock.ffvalid()[0]:
            print "No valid financial data"
            return

        print "addings: ", stock.addings()

        print "select adding:", stock.a()
        print "pershareearning:", stock.e()
        print "price:", stock.price()
        print "e/q:", stock.eq()
        print "q(reasonable price):", stock.q()
        print "dratio(price adding predict):", stock.dratio()



    def select(self, ids):
        no = 1
        for i in ids:
            print no, i, Globals.get_instance().getstockidnamemapping().getname(i)
            no += 1

        while True:
            choice = raw_input("Please select:")
            try:
                k = int(choice)
                if k < no and k > 0:
                    return ids[k - 1]
            except:
                pass

