import configparser

class Conf:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('config.ini')
    def GetConfig(self):
        return self.conf
