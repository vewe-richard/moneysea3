from moneyseav3.resources.stockidnamemapping import StockIdNameMapping


class Globals:
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self._stockidnamemapping = StockIdNameMapping()
        sim = self._stockidnamemapping.getmap()
        self._stocks = sim


    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Globals()
        return cls.INSTANCE


    # return dict of {stockid:Stock}. Financial data may not be ready.
    def stocks(self):
        return self._stocks



if __name__ == "__main__":
    pass
