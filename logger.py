import logging, os, sys
from logging.handlers import RotatingFileHandler

cur_dir = os.path.abspath(os.curdir)
sys.path.append(cur_dir)
PROJECT_HOME = cur_dir

def get_logger(name):
    """
    Args:
        name(str): 생성할 로그 파일명입니다

    Returns:
        생성된 logger 객체를 반환합니다
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    rotate_handler = RotatingFileHandler(PROJECT_HOME+"/logs/"+name+".log", 'a', 1024*1024*5, 5)
    formatter = logging.Formatter('[%(levelname)s]-%(ascname)s-%(filename)s:%(lineno)s:%(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    rotate_handler.setFormatter(formatter)
    logger.addHandler(rotate_handler)
    return logger