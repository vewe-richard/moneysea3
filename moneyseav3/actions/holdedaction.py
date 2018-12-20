
from moneyseav3.actions.baseaction import BaseAction

class HoldedAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "fitting"

    def summary(self):
        return "try fitting to find suitable n, p value"


    def description(self):
        return '''
SYNOPSIS: 
    python moneysea fitting <type> [n=x p=x]

DESCRIPTION:
    draw fitting graph for the specific type

OPTIONS:
    <type>
        stock type
    [n=x p=x]
        n and p value, default n=5, p=0.08
'''


    def run(self, args, opts):
        pass




