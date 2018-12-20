
from moneyseav3.actions.baseaction import BaseAction

class TypesAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "types"

    def summary(self):
        return "show all stock types"


    def description(self):
        return '''
SYNOPSIS:
    python monsea types [list | dump | show] [<args>]
DESCRIPTION:
    show all stock types

COMMAND:
    list
        list all types
    dump type
        dump all stock of specific type
    show stockid
        show type of the specific stock 
'''


    def run(self, args, opts):
        pass










