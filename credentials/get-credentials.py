"""
본 스크립트는 레디스에 설정값들을 올릴 수 있도록 도와주는 프로그램입니다.
"""

#import argparse
#
#parser = argparse.ArgumentParser()
#parser.add_argument('--ip', default='127.0.0.1', help="Set IP Address of Redis Server")
#parser.add_argument('--port', default='6379', help="Set Port of Redis Server")
#parser.add_argument('--dir', default='conf/config.ini', help="File location of Configuration file")
#parser.add_argument('--cred', help="Your Cred. Key for Secure the credentials")
#args = parser.parse_args()
#

import configparser
import json
import hashlib
arr = {}
conf = configparser.ConfigParser()
conf.read('conf/config.ini')
for sect in conf.sections():
    for key in conf[str(sect)]:
        arr[str(sect)+':'+str(key)] = conf[str(sect)][str(key)]
print(arr.keys())