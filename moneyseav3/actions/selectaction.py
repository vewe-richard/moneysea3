
from moneyseav3.actions.baseaction import BaseAction

class SelectAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "price"

    def summary(self):
        return "update prices"


    def description(self):
        return '''
SYNOPSIS:
    python monsea price 
DESCRIPTION:
    update prices of all stocks
'''


    def run(self, args, opts):
        pass



