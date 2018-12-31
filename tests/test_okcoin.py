import unittest
from machine.okcoin import OKCoin

class OKCoinModuleTest(unittest.TestCase):
    
    def setUp(self):
        self.okcoin = OKCoin()
    
    def test_getticker(self):
        """티커 주문 가져오기"""
        self.ticker = self.okcoin.get_ticker(symbol='btc_krw')
        assert self.ticker
        print(self.ticker)
    
    def test_getorderinfo(self):
        """주문정보 가져오기"""
        # 주문한 정보가 없으므로 -1 추가해서 데이터 가져오는 명령을 내림
        self.orderinfo = self.okcoin.get_order_info(symbol='btc_krw', order_id="-1") 
        assert self.orderinfo
        print(self.orderinfo)
    
    def test_wallet_status(self):
        """지갑 상태 가져오기"""
        self.userinfo = self.okcoin.get_wallet_status()
        assert self.userinfo
        print(self.userinfo)
    
    def test_Selected_order(self):
        """지정가 주문 테스트"""
        self.selected_order = self.okcoin.order_limit(symbol='btc_krw', sell_type='sell', price=1000, amount="0.1")
        assert self.selected_order
        print(self.selected_order)

    def test_market_sell(self):
        """시장가 주문 테스트"""
        self.order_market = self.okcoin.order_market(price=1200, symbol='btc_krw', sell_type='buy_market')
        assert self.order_market
        print(self.order_market)

    def test_cancel_order(self):
        """주문 취소 테스트"""
        self.order_cancel = self.okcoin.cancel_order(order_id="123456", symbol='btc_krw')
        assert self.order_cancel
        print(self.order_cancel)

if __name__ == '__main__':
    unittest.main()