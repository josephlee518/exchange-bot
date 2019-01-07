"""
본 스크립트는 레디스에 설정값들을 올릴 수 있도록 도와주는 프로그램입니다.
"""
import os
os.path.join('../') # 폴더에서 실행할 경우 파일을 읽어들일 수 없음을 해결하기 위한 스크립트
import configparser
import redis
r = redis.Redis("172.17.0.2")
conf = configparser.ConfigParser()
if bool(conf.read('conf/config.ini')) == True:
        conf.read('conf/config.ini')
else:
        raise Exception("There are No Config Files!")
for sect in conf.sections():
    for key in conf[str(sect)]:
        r.set(str(sect)+':'+str(key), conf[str(sect)][str(key)])