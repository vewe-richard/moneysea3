
from moneyseav3.actions.baseaction import BaseAction
from moneyseav3.tests.verifyaction import VerifyAction
from moneyseav3.tests.stataction import StatAction

class TestAuto(BaseAction):
    def cmd(self):
        return "auto"

    def summary(self):
        return "auto run all test suits"

    def run(self, args, opts):
        from moneyseav3.tests.verify.prices import PricesVerify
        allv = [PricesVerify]

        results = {}
        for c in allv:
            obj = c()
            obj.autorun()
            results[obj.cmd()] = obj.result()

        print ""
        print "Auto Tests results:"
        for r in results:
            print "\t", r, ":", results[r]

class ShowAction(BaseAction):
    def cmd(self):
        return "show"

    def summary(self):
        return "show test commands"

    def description(self):
        return "description"

    def run(self, args, opts):
        ta = TestAction()
        try:
            if "--verbose" in opts[0]:
                ta.details()
                return
        except:
            pass
        ta.usage()

class TestAction(BaseAction):
    def __init__(self):
        self._actions = [TestAuto, VerifyAction, StatAction, ShowAction]
        pass

    def cmd(self):
        return "test"

    def summary(self):
        return "perform test command"


    def description(self):
        return '''
SYNOPSIS: 
    python moneysea [--verbose] test command

DESCRIPTION:
    test command

OPTIONS:
    <cmd>
        test command, such as show to show all test command, default is show
    --verbose
        show all test commands
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

    def details(self):
        print "Usage: python moneysea test command [<args>]"
        for action in self._actions:
            obj = action()
            print "\t" + obj.cmd()
            try:
                ll = obj.actionsdes()
                for item in ll:
                    print "\t\t", item
            except:
                pass
            print ""


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







