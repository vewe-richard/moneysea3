# coding=utf-8

class Config:
    #-------------------------- File path --------------------------
    #input
    INPUT_DIR = "input"

    STOCK_ID_NAME_MAP_SHA = "input/common/stock_id_name_map/sha"
    STOCK_ID_NAME_MAP_SZ = "input/common/stock_id_name_map/sz"
    STOCK_ID_NAME_MAP_OPEN = "input/common/stock_id_name_map/open"

    CURRENT_HOLDED_PATH = "input/holded"

    STOCKS_PATH_NETEASE = "input/stocks/netease"
    STOCKS_PATH_THS = "input/stocks/ff10jqka"

    CLASSFY_PATH = "input/classfy"
    CLASSFY_XML = "input/classfy/classfy.xml"

    PRICES_PATH = "input/prices/recent"
    PRICES_PATH2 = "input/prices/historyprices/"
    PRICES_PATH3 = "input/prices/historypricesshares/"

    #output
    OUTPUT = "output/"

    #minimal profit request
    MINIMAL_PROFIT = 1000000

    # should be moved to default.xml
    N = 5
    P = 0.08
    def __init__(self):
        pass
