# coding=utf-8
# 指数：
# http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=20150911&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER
import shlex
import subprocess
import os
import sys
from moneyseav3.globals import Globals

class HistoryPrices:
    def run(self):
        ids = Globals.get_instance().stocks().keys()

        os.chdir("./output/historyprices/")
        # for each stock
        for idx in ids:
            self.downloadstock(idx)
        # download index
        # SZSE.399001 深证成指, SZSE.399006 创业板指, SHSE.000001 上证综指, SZSE.399300 沪深300

        for idx in ("1399001", "1399006", "0000001", "0000300"):
            self.downloadindex(idx)
        os.chdir("../../")
        pass

    def downloadstock(self, idx):
        if idx[0] == '6':
            self.downloadshastock(idx)
        else:
            self.downloadszstock(idx)

    def downloadshastock(self, idx):
        cmd = self.wgetcmd() + '-O ' + idx + ".csv " 
        cmd += 'http://quotes.money.163.com/service/chddata.html?code=0' + idx + '&end=20181130'

        call_params = shlex.split(cmd)
        ret = subprocess.call(call_params)
        if ret != 0:
            print "Download error(", ret, "):" + idx

    def downloadszstock(self, idx):
        cmd = self.wgetcmd() + '-O ' + idx + ".csv " 
        cmd += 'http://quotes.money.163.com/service/chddata.html?code=1' + idx + '&end=20181130'

        call_params = shlex.split(cmd)
        ret = subprocess.call(call_params)
        if ret != 0:
            print "Download error(", ret, "):" + idx

    def downloadindex(self, idx):
        cmd = self.wgetcmd() + '-O ' + idx + ".csv " 
        cmd += 'http://quotes.money.163.com/service/chddata.html?code=' + idx + '&end=20181227'

        call_params = shlex.split(cmd)
        ret = subprocess.call(call_params)
        if ret != 0:
            print "Download error(", ret, "):" + idx

    def wgetcmd(self):
        return 'wget --user-agent="Mozilla/5.0 （Windows; U; Windows NT 6.1; en-US） AppleWebKit/534.16 （KHTML， like Gecko） Chrome/10.0.648.204 Safari/534.16" -nv --tries=3 --timeout=5 '


