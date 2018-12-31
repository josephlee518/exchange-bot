"""
데이터 수집을 위한 스케쥴러 구현
"""
from machine.db.MongoDB import MongoDB
from datetime import datetime
from machine.okcoin import OKCoin

if __name__ == '__main__':
    okcoin = OKCoin()
    result_etc = okcoin.get_ticker(symbol="etc_krw")
    result_eth = okcoin.get_ticker(symbol="eth_krw")
    result_btc = okcoin.get_ticker(symbol="btc_krw")
    result_xrp = okcoin.get_ticker(symbol="xrp_krw")
    result_bch = okcoin.get_ticker(symbol="bch_krw")
    result_btg = okcoin.get_ticker(symbol="btg_krw")