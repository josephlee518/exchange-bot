import unittest
from pusher import telegram

class TestSlack(unittest.TestCase):
    def setUp(self):
        self.pusher = telegram.PushTelegram()
    
    def test_send_message(self):
        self.pusher.send_message("me", "This is the 테스트 MSG")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()