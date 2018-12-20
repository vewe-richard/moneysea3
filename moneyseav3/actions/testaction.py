
from moneysea.actions.baseaction import BaseAction
from moneysea.test.stasticsfinancials import StasticsFinancials
from moneysea.test.ways import Ways

class ShowAction(BaseAction):
    def cmd(self):
        return "show"

    def summary(self):
        return "show test commands"

    def description(self):
        return "description"

    def run(self, args, opts):
        ta = TestAction()
        ta.usage()

class TestAction(BaseAction):
    def __init__(self):
        self._actions = [StasticsFinancials, Ways, ShowAction]
        pass

    def cmd(self):
        return "test"

    def summary(self):
        return "perform test command"


    def description(self):
        return '''
SYNOPSIS: 
    python moneysea test command

DESCRIPTION:
    test command

OPTIONS:
    <cmd>
        test command, such as show to show all test command, default is show
'''

    def getaction(self, cmd):
        for action in self._actions:
            obj = action()
            if cmd == obj.cmd():
                return obj
        return None

    def usage(self):
        print "Usage: python moneysea test command [<args>]"
        for action in self._actions:
            obj = action()
            print "\t" + obj.cmd() + "\t\t" + obj.summary()


    def run(self, args, opts):
        if len(args) == 0:
            cmd = "show"
            nargs = args
        elif args[0] == "help":
            cmd = "show"
            nargs = args[1:]
        else:
            cmd = args[0]
            nargs = args[1:]

        a = self.getaction(cmd)
        if a == None:
            print "Unknown test command"
            return
        a.run(nargs, opts)
        pass







