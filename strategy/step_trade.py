import sys
import datetime
import traceback
from machine.db.MongoDB import MongoDB # For Database Processing
from machine.okcoin import OKCoin # For Order Processing
from pusher import telegram
from logger import get_logger
from strategy.base_strategy import Strategy
logging = get_logger("step_trade")

class StepTrade(Strategy):
    def __init__(self, machine=None, db_handler=None, strategy=None, currency_type=None, pusher=None):
        if machine is None or db_handler is None or currency_type is None or strategy is None or pusher is None:
            raise Exception("Need to machine, db, currency type, strategy")
        #if isinstance(machine, KorbitMachine):
        #    logging.info("Korbit Machine")
        #    self.currency_type = currency_type+"_krw"
        #elif isinstance(machine, CoinoneMachine):
        #    logging.info("Coinone Machine")
        if isinstance(machine, OKCoin):
            logging.info("OKCoin Machine")
            self.currency_type = currency_type+"_krw"
        self.machine = machine
        self.pusher = pusher
        self.db_handler = db_handler
        result = self.db_handler.find_item({"name":strategy})
        self.params = result[0]
        if self.params["is_active"] == "inactive":
            logging.info("inactive")
            return
        self.token = self.machine.set_token() # 오케이코인에서는 이 함수를 정의하지 않았음
        logging.info(self.token)
        logging.info(self.currency_type)
        last = self.machine.get_ticker(self.currency_type)
        self.last_val = int(last["buy"])

    def check_buy_ordered(self):
        buy_orders = self.db_handler.find_item({"currency":self.currency_type, "status":"BUY_ORDERED"})
        for item in buy_orders:
            logging.info(item)
            order_result = self.machine.get_order_info(symbol=self.currency_type, order_id=item["buy_order_id"])
            logging.info(order_result)
            if len(order_result) > 0 and order_result[0]["status"] == "filled" and order_result[0]["price"] == str(item["buy"]):
                order_result_dict = order_result[0]
                real_buy_amount = float(order_result_dict["filled_amount"])-float(order_result_dict["fee"])
                real_buy_value = float(order_result_dict["avg_price"])
                completed_time = int(order_result_dict["last_filled_at"]/1000)
                fee = float(order_result_dict["fee"])
                if order_result_dict["side"] == "bid":
                    self.update_trade_status(item_id={"_id":item["_id"]},value={"status":"BUY_COMPLETED",
                    "real_buy_amount": real_buy_amount,
                    "buy_completed_time": completed_time,
                    "real_buy_value": real_buy_value,
                    "buy_fee":fee,
                    "error":"success"})
                    self.pusher.send_message("#push", "buy_completed: "+str(item))
                elif len(order_result) > 0 and order_result[0]["status"] == "unfilled" and order_result[0]["price"] == str(item["buy"]):
                    if int(item["buy"])+int(self.params["step_value"]) <= self.last_val:
                        logging.info("Cancel Order")
                        logging.info(item)
                        # cancel order
                        try:
                            self.order_cancel_transaction(currency_type=currency_type, item=item)
                        except:
                            error = traceback.format_exc()
                            logging.info(error)
                            self.update_trade_status(item_id={"_id":item["_id"]}, value={"error":"failed"})
                            self.pusher.send_message("#push", "Error Cancel:"+str(item))
                elif len(order_result) == 0:
                    self.update_trade_status(item_id={"_id": item["_id"]}, value={"status": "CANCEL_ORDERED"})

    def check_buy_completed(self):
        buy_completed = self.db_handler.find_item({"currency":self.currency_type, "status":"BUY_COMPLETED"})
        logging.info("BUY COMPLETED!")
        for item in buy_completed:
            logging.info(item)
            try:
                self.order_sell_transaction(currency_type=self.currency_type, item=item)
            except:
                error = traceback.format_exc()
                logging.info(error)
                self.update_trade_status(item_id={"_id": item["_id"]}, value={"error":"failed"})
    
    def check_sell_ordered(self):
        sell_orders = self.db_handler.find_item({"currency": self.currency_type, "status": "SELL_ORDERED"})
        for item in sell_orders:
            logging.info(item)
            if "sell_order_id" in item:
                order_result = self.machine.get_order_info(symbol=self.currency_type, order_id=item["sell_order_id"])
                if order_result is not None:
                    logging.info(order_result)
                else:
                    continue
            if len(order_result) > 0 and order_result[0]["status"] == "filled" and order_result[0]["price"] == str(item["desired_value"]):
                order_result_dict = order_result[0]
                real_sell_amount = float(order_result_dict["filled_amount"])
                real_sell_value = float(order_result_dict["avg_price"])
                completed_time = int(order_result_dict["last_filled_at"]/1000)
                fee = float(order_result_dict["fee"])
                if order_result_dict["side"] == "ask":
                    self.update_trade_status(item_id={"_id": item["_id"]}, value={"status": "SELL_COMPLETED",
                    "real_sell_amount": real_sell_amount,
                    "sell_completed_time": completed_time,
                    "real_sell_value": real_sell_value,
                    "sell_fee": fee})
                    self.pusher.send_message("#push", "sell_completed:"+str(item))
            elif len(order_result) > 0 and order_result[0]["status"] == "unfilled" and order_result[0]["price"] == str(item["desired_value"]):
                if int(item["desired_value"]) > self.last_val*1.15:
                    print(item)
                    self.order_cancel_transaction(currency_type=self.currency_type, item=item)
                    self.update_trade_status(item_id={"_id": item["_id"]}, value={"status": "KEEP_ORDERED"})
    
    def check_sell_completed(self):
        sell_completed = self.db_handler.find_item({"currency":self.currency_type, "$or":[{"status":"SELL COMPLETED"}, {"status": "CANCEL_ORDERED"}]})
        for item in sell_completed:
            self.db_handler.insert_item(data=item)
            self.db_handler.delete_items(condition={"_id": item["id"]})

    def check_keep_ordered(self):
        keeped_orders = self.db_handler.find_item({"currency": self.currency_type, "status": "KEEP_ORDERED"})
        for item in keeped_orders:
            if int(item["desired_value"])*0.9 < self.last_val:
                self.order_sell_transaction(currency_type=self.currency_type, item=item)
                logging.info("sell order from keeped"+str(item["_id"]))

    def scenario(self):
        now = datetime.datetime.now()
        five_min_ago = now - datetime.timedelta(minutes=5)
        five_min_ago_timestamp = int(five_min_ago.timestamp())
        pipeline_5m = [
            {"$match": {"timestamp": {"$gt": five_min_ago_timestamp}, "coin":self.currency_type}},
            {"$group": {"_id": "$coin", "min_val": {"$min":"$price"}, "max_val": {"$max":"$price"}, "sum_val": {"$sum":"$amount"}}}
        ]
        five_min_result = self.db_handler.aggregate(pipeline=pipeline_5m)
        for item in five_min_result:
            five_max_val = int(item["max_val"])
            five_min_val = int(item["min_val"])
            five_sum_val = int(item["sum_val"])
            five_sum_avg_val = int(item["sum_val"]/5)
            five_gap = five_max_val - five_min_val
        if float(five_min_val) < float(self.last_val):
            self.pusher.send_message("#push", "Down Stream 5 min_val={0}, last_val={1}".format(str(five_min_val), str(self.last_val)))
            return
        if float(five_max_val) > float(self.last_val):
            self.pusher.send_message("#push", "Up Stream 5 min_val={0}, last_val={1}".format(str(five_min_val), str(self.last_val)))
            logging.info("buy_price:"+str(self.last_val))
            my_orders = self.db_handler.find_item({"currency": self.currency_type, "$or":[{"status": "BUY_ORDERED"}, {"status":"SELL_ORDERED"}, {"status":"BUY_COMPLETED"}], "buy":{"$gte": self.last_val-int(self.params["step_value"]), "$lte": self.last_val-int(self.params["step_value"])}})
            if my_orders.count() > 0:
                logging.info("Exists order in same place")
                for order in my_orders:
                    logging.info(order)
            else:
                logging.info("BUY Order")
                self.item={"buy":str(self.last_val), "buy_amount":self.params["buy_amount"], "currency":self.currency_type}
                self.item["desired_value"] = int(self.last_val+int(self.params["target_profit"])/float(self.params["buy_amount"]))
                logging.info(self.item)
                wallet = self.machine.get_wallet_status()
                if int(wallet["free"]["krw"]) > int(self.last_val*float(self.params["buy_amount"])):
                    self.order_buy_transaction(machine=self.machine, db_handler=self.db_handler, currency_type=self.currency_type, item=self.item)
                    self.check_buy_ordered()
                else:
                    logging.info("krw is short") 
    
    def check_my_order(self):
        self.check_buy_ordered()
        self.check_buy_completed()
        self.check_sell_ordered()
        self.check_sell_completed()
        self.check_keep_ordered()

    def run(self):
        if self.params["is_active"] == "active":
            self.check_my_order()
            self.scenario()
        else:
            logging.info("inactive")

if __name__ == '__main__':
    mongodb = MongoDB.MongoDB()
    okc = OKCoin()
    pusher = telegram.PushTelegram()
    if len(sys.argv) > 0:
        trader = StepTrade(machine=OKCoin, db_handler=mongodb, strategy=sys.argv[1], currency_type=sys.argv[2], pusher=pusher)
        trader.run()