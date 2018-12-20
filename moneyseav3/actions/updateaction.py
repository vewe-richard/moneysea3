
from moneyseav3.actions.baseaction import BaseAction

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
    python moneyseav3 update [prices | financial | predict]
DESCRIPTION:
    update stock data

COMMAND:
    prices 
        update prices
    financial
        update financial data
    predict
        update stock predict report
'''


    def run(self, args, opts):
        pass










