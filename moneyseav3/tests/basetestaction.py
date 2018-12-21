from moneyseav3.actions.baseaction import BaseAction

class BaseTestAction(BaseAction):
    def __init__(self):
        self._actions = []
        pass

    def cmd(self):
        return "basetestaction"

    def summary(self):
        return "base test action"

    def getaction(self, cmd):
        for action in self._actions:
            obj = action()
            if cmd == obj.cmd():
                return obj
        return None

    def usage(self):
        for action in self._actions:
            obj = action()
            print "\t" + obj.cmd() + "\t\t" + obj.summary()

    def actionsdes(self):       #description of actions
        ll = []
        for action in self._actions:
            obj = action()
            ll.append(obj.cmd() + "\t\t" + obj.summary())
        return ll


    def run(self, args, opts):
        if len(args) == 0 or args[0] == "help" or args[0] == "show":
            self.usage()
            return
        else:
            cmd = args[0]
            nargs = args[1:]

        a = self.getaction(cmd)
        if a == None:
            print "Unknown command"
            return
        a.run(nargs, opts)
        pass


