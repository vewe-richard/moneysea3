
from moneyseav3.actions.baseaction import BaseAction
class BaseTestUnit(BaseAction):
    def __init__(self):
        BaseAction.__init__(self)
        self._result = False

    def result(self):
        return self._result

    def autorun(self):
        self.run(None, None)
