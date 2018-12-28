import logging
import configparser

class log:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read('conf/config.ini')
        self._log_dir = self._config['LOGGING']['directory']
        self._log_filename = self._config['LOGGING']['filename']
        logging.basicConfig(filename="%s/%s.log" % (self._log_dir, self._log_filename),level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    def log(self, info):
        logging.info(info)