"""
오케이코인 코리아 래퍼

본 래퍼를 사용함으로써 생기는 문제는 본인에게 있습니다

SEUNGWOO LEE, ALL RIGHTS RESERVED.
"""
import configparser
import hashlib
import urllib
import requests
import time

class OKCoin:
    
    def __init__(self, mode='normal'):
        self._API_URL = 'https://www.okcoinkr.com/api/'
        self._config = configparser.ConfigParser()
        self._config.read('../conf/config.ini')
        self.CLIENT_API_KEY = self._config['OKCOIN']['okcoin_api_key']
        self.CLIENT_API_SECRET = self._config['OKCOIN']['okcoin_secret_key']
    
    def get_ticker(self, symbol=None):
        """
        마지막 거래정보(Tick)을 구하는 매서드입니다.
        Args:
            Currency Type(str): 화폐의 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어 있습니다
        Returns:
            결과를 딕셔너리로 반환합니다.
            결과 필드는 date, buy, high, last, low, sell, volume 으로 구성됩니다.
        """
        if symbol is None:
            raise Exception('Need To Currency Type')
        time.sleep(1)
        params = {'symbol':symbol}
        res = requests.get(self._API_URL+'v1/ticker.do', params=params)
        response_json = res.json()
        result = {}
        result["currency"] = symbol
        result["timestamp"] = str(response_json["date"])
        result["buy"] = response_json["ticker"]["buy"]
        result["high"] = response_json["ticker"]["high"]
        result["last"] = response_json["ticker"]["last"]
        result["low"] = response_json["ticker"]["low"]
        result["sell"] = response_json["ticker"]["sell"]
        result["volume"] = response_json["ticker"]["vol"]
        return result
    
    def get_order_info(self, symbol=None, order_id=None):
        """
        거래채결 정보를 가져옵니다.
        Args:
            currency_type(str): 화폐의 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어 있습니다.
            order_id(long): 거래 ID를 입력받습니다. -1을 입력값으로 집어넣을 수도 있으나 여기에서는 거래 ID를 입력받습니다.
        Returns:
            결과를 딕셔너리로 반환합니다. 에러가 있는 경우에는 에러 숫자가 출력됩니다.
            TODO: 결과 필드 체크 후 이 문서 변경할 것

        """
        if symbol is None:
            raise Exception('Need to Currency Type')
        if order_id is None:
            raise Exception('Need to Order ID')
        time.sleep(1)
        params = {'api_key':self.CLIENT_API_KEY, 'order_id':order_id, 'symbol':symbol}
        sign = hashlib.md5((urllib.parse.urlencode(params)+"&secret_key=%s" % (self.CLIENT_API_SECRET)).encode('utf-8')).hexdigest().upper()
        params['sign'] = sign
        res = requests.post(self._API_URL+'v1/order_info.do', params=params)
        response_json = res.json()
        """
        본 주문은 2개월까지만 리턴됩니다.
        """
        return response_json

    def get_wallet_status(self):
        """
        지갑에 들어있는 상태를 알아내는 함수입니다.
        Args: None
        Response: 각 화폐에 대한 상태값을 3단계로 나누어 JSON 카테고리화하여 리턴합니다 (funds, free, freezed)
        """
        params = {'api_key':self.CLIENT_API_KEY}
        sign = hashlib.md5((urllib.parse.urlencode(params)+"&secret_key=%s" % (self.CLIENT_API_SECRET)).encode('utf-8')).hexdigest().upper()
        params['sign'] = sign
        res = requests.post(self._API_URL+'v1/userinfo.do', params=params)
        response_json = res.json()
        return response_json

    def order_limit(self, sell_type=None, price=None, amount=None, symbol=None):
        """
        지정가 주문 및 판매를 생성하는 코드입니다. 최소 주문가를 넘어야 합니다. 수수료는 문서를 참고하시기 바랍니다.
        최소주문 가격은 사이트를 참고하세요. 최소주문가는 실시간으로 변동될 수 있습니다.
        Args:
            symbol(str): token_krw
            type(str): buy, sell
            price(double): range (>=0, <=1000000)
            amount(str): amount of currency
        Response:
            result(bool): 거래가 잘 이루어졌는지 상태값을 리턴합니다 (true, false)
            order_id(long): 거래가 정상적으로 이루어졌다면, 본 거래에 대한 ID를 리턴합니다
        """
        if sell_type is None or price is None or amount is None or symbol is None:
            raise Exception("Plase Check your Input")
        params = {'amount':amount, 'api_key':self.CLIENT_API_KEY, 'price':price, 'symbol':symbol, 'type': sell_type}
        sign = hashlib.md5((urllib.parse.urlencode(params)+"&secret_key=%s" % (self.CLIENT_API_SECRET)).encode('utf-8')).hexdigest().upper()
        params['sign'] = sign
        res = requests.post(self._API_URL+'v1/trade.do', params=params)
        response_json = res.json()
        return response_json
    
    def order_market(self, price=None, symbol=None, sell_type=None):
        """
        시장가 주문 및 판매를 생성하는 코드입니다. 시장가격을 넘어야 하며 수수료는 문서를 참고하시기 바랍니다.
        가격은 1호 매수가격보다 커야 합니다.
        Args:
            symbol(str): token_krw
            type(str): buy_market(주문) or sell_market(판매)
            price(double): more than market price
        Response:
            result(bool): status of exchange has success (true, false)
            order_id(long): if order or sell has success, it returns id
        """
        if price is None or symbol is None or sell_type is None:
            raise Exception("Please check your Input!")
        params = {'api_key':self.CLIENT_API_KEY, 'price':price, 'symbol':symbol, 'type':sell_type}
        sign = hashlib.md5((urllib.parse.urlencode(params)+"&secret_key=%s" % (self.CLIENT_API_SECRET)).encode('utf-8')).hexdigest().upper()
        params['sign'] = sign
        res = requests.post(self._API_URL+'v1/trade.do', params=params)
        response_json = res.json()
        return response_json

    def cancel_order(self, order_id=None, symbol=None):
        """
        앞서 시장가 혹은 지정가 주문했던 것을 취소하는 코드입니다.
        Args:
            order_id(str): order_id (주문 ID, 최대 3개까지 동시에 집어넣을 수 있고, 컴마로 구분)
            ※ Array로 넣으면 자동으로 변환합니다.
            symbol(str): token_krw
        Response:
            success(str): 주문 취소에 성공한 ID
            error(str): 주문 취소에 실패한 ID
        """
        if order_id is None or symbol is None:
            raise Exception("Please check your Input!")
        else:
            pass
        params = {'api_key':self.CLIENT_API_KEY, 'order_id':order_id, 'symbol':symbol}
        sign = hashlib.md5((urllib.parse.urlencode(params)+"&secret_key=%s" % (self.CLIENT_API_SECRET)).encode('utf-8')).hexdigest().upper()
        params = {'api_key':self.CLIENT_API_KEY, 'order_id':order_id, 'sign':sign, 'symbol':symbol}
        res = requests.post(self._API_URL+'v1/cancel_order.do', params=params)
        response_json = res.json()
        return response_json
