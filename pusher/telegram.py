import configparser
from telethon import TelegramClient

class PushTelegram():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        api_id = config['TELEGRAM']['api_id']
        api_hash = config['TELEGRAM']['api_hash']
        self.telegram = TelegramClient("autotrading", api_id, api_hash)
        assert self.telegram
        self.telegram.connect()
    
    def send_message(self, username=None, message=None):
        self.telegram.send_message(username, message)