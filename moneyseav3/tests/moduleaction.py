from moneyseav3.tests.basetestaction import BaseTestAction
from moneyseav3.tests.module.fadatatest import FadataTest


class ModuleAction(BaseTestAction):
    def __init__(self):
        self._actions = [FadataTest,]
        pass

    def cmd(self):
        return "module"

    def summary(self):
        return "module test"

