"""
기본적인 트레이딩을 위한 실행파일입니다.
"""
import datetime
from machine.db.MongoDB import MongoDB # For Database Processing
mongo = MongoDB.MongoDB()
from machine.okcoin import OKCoin # For Order Processing
okc = OKCoin()
from logger import get_logger
logging = get_logger("base_strategy")

class Strategy:
    def __init__(self):
        pass

    def update_trade_status(self, item_id=None, value=None):
        """현재 상태를 업데이트하는 메서드

        Args:
            db_handler(obj): 대상 데이터베이스 모듈 객체
            item_id(dict): 업데이트 조건
            value(dict): 업데이트하려는 문서의 칼럼과 값
        """
        if value is None or item_id is None:
            raise Exception("Need to Buy Value or Value is None")
        mongo.update_items(item_id, {"$set":value})

    def order_buy_transaction(self, machine=None, db_handler=None, currency_type=None, item=None):
        """매수주문과 함께 데이터베이스에 필요한 데이터를 입력하는 메서드
        Args:
            machine(obj): 매수주문하는 거래소 모듈 객체
            db_handler(obj): 매수주문 정보를 입력할 데이터베이스 모듈 객체
            currency_type(str): 매수주문하려는 화폐 종류
            item(dict): 매수 완료 후 데이터베이스에 저장하려는 데이터
            order_type(str): 매수 방법

        Returns:
            order_id(str): 매수주문 완료 후의 주문 id
        """
        if currency_type is None or item is None:
            raise Exception("Need to Param")
        """
        OKCoin에서는 시장가 주문과 지정가 주문을 지원하고 있는데, 지금은 Step Trade 방식을 사용하고 있으니 시장가 주문만을 사용하여

        진행해보도록 하겠습니다. 다른 주문같은 경우에는 지정가주문 및 함수를 바꾸어주어야 합니다.
        """
        result = okc.order_limit(sell_type="buy", price=str(item["buy"]), amount=str(item["buy_amount"]), symbol=currency_type)
        if result['result'] == "true":
            mongo.insert_item({"status": "BUY_ORDERED",
            "currency": currency_type,
            "buy_order_id": str(result["order_id"]),
            "buy_amount": float(item["amount"]),
            "buy_order_time": int(datetime.datetime.now().timestamp()),
            "desired_value": int(item["desired_value"]),
            "machine":str(machine)})
            return result["order_id"]
        else:
            logging.warning(result)
            logging.warning(item)
            mongo.update_items({"_id": item["_id"]}, {"error": "failed"})
            return None

    def order_sell_transaction(self, currency_type=None, item=None):
        """매도주문과 함께 데이터베이스에 필요한 데이터를 업데이트하는 메서드
        Args:
            machine(obj): 매도주문하려는 거래소 모듈 객체
            db_handler(obj): 매도주문 정보를 입력할 데이터베이스 모듈 객체
            currency_type(str): 매도주문하려는 화폐 종류
            item(dict): 매도 완료 후 데이터베이스에 저장하려는 데이터
            order_type(str): 매도 방법

        Returns:
            order_id(str): 매도주문 완료 후의 주문 id
        """
        if currency_type is None or item is None:
            raise Exception("Need to Param")
        result = okc.order_limit(sell_type="sell", price=str(item["desired_value"]), amount=str(round(item["real_buy_amount"], 8)))
        if result['result'] == "true":
            mongo.update_items({"_id":item["_id"]},
            {"$set": {"status": "SELL_ORDERED", 
             "desired_value": int(item["desired_value"]), 
             "sell_order_id": str(result["order_id"]), 
             "error": "success"}})
            return result["order_id"]
        else:
            logging.warning(result)
            logging.warning(item)
            mongo.update_items({"_id": item["_id"]}, {"error": "failed"})
            return None


    def order_cancel_transaction(self, currency_type=None, item=None):
        """취소주문과 함께 데이터베이스에 필요한 데이터를 업데이트하는 메소드
        Args:
            machine(obj): 취소주문하는 거래소 모듈 객체
            db_handler(obj): 취소주문 정보를 입력할 데이터베이스 모듈 객체
            currency_type(str): 취소주문하려는 화폐 종류
            item(dict): 취소주문에 필요한 데이터
        
        Returns:
            order_id(str): 취소 완료 후의 주문 id
        """
        if currency_type is None or item is None:
            raise Exception("Need to Param")
        if item["status"] == "BUY_ORDERED":
            result = okc.cancel_order(order_id=item["buy_order_id"], symbol=currency_type)
            if result["result"] == "true":
                mongo.update_items({"_id":item["_id"]}, {"$set": {"status": "CANCEL_ORDERED", "cancel_order_time": int(datetime.datetime.now().timestamp()), "error": "success"}})
                return item["buy_order_id"]
            else:
                logging.warning(result)
                logging.warning(result)
                return None
        elif item["status"] == "SELL_ORDERED":
            result = okc.cancel_order(order_id=item["sell_order_id"], symbol=currency_type)
            if result["result"] == "true":
                mongo.update_items({"_id": item["_id"]}, {"$set": {"status": "CANCEL_ORDERED", "cancel_order_time": int(datetime.datetime.now().timestamp()), "error":"success"}})
                return item["sell_ordered_id"]
            else:
                logging.warning(result)
                logging.warning(item)
                return None