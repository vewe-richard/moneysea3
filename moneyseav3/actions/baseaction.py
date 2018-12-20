class BaseAction:
    def __init__(self):
        pass

    def cmd(self):
        return "base"

    def summary(self):
        return "summary"


    def description(self):
        return "description"


    def run(self, args, opts):
        print args, opts
