
from moneyseav3.actions.baseaction import BaseAction
from moneyseav3.tools.historyprices import HistoryPrices
from moneyseav3.tools.historypricesshare import HistoryPricesShare
from moneyseav3.tools.prices import Prices

class UpdateAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "update"

    def summary(self):
        return "update stock data"


    def description(self):
        return '''
SYNOPSIS:
    python moneysea update [prices | financial | predict | historyprices]
DESCRIPTION:
    update stock data

COMMAND:
    prices 
        update prices
    financial
        update financial data
    predict
        update stock predict report
    historyprices
        download history prices
    historypricesshare
        change historyprices to prices and share change
'''

    def usage(self):
        print self.description()

    def run(self, args, opts):
        if len(args) < 1:
            print "Please specify resources to update or download"
            self.usage()
            return
        if args[0] == "historyprices":
            hp = HistoryPrices()
            hp.run()
        elif args[0] == "prices":
            p = Prices()
            p.run()
        elif args[0] == "historypricesshare":
            hps = HistoryPricesShare()
            hps.run()
        else:
            print "Unknown update command:" + args[0]
            self.usage()
            return
        pass










