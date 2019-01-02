from machine.db.MongoDB import MongoDB
from machine.okcoin import OKCoin
from datetime import datetime
from celery import Celery, Task

app = Celery('currency_info', broker='redis://172.17.0.3/')

app.conf.beat_schedule = {
    'app-every-1-min': {
        'task': 'scheduler_currency_price.get_currency_info',
        'schedule': 60.0,
        'args': {}
    }, 
}

@app.task
def get_currency_info():
    okcoin = OKCoin()
    mongodb = MongoDB.MongoDB()
    result_btc = okcoin.get_ticker('btc_krw')
    result_xrp = okcoin.get_ticker('xrp_krw')
    result_auto = okcoin.get_ticker('auto_krw')
    result_etc = okcoin.get_ticker('etc_krw')
    result_trx = okcoin.get_ticker('trx_krw')
    result_bch = okcoin.get_ticker('bch_krw')
    result_bsv = okcoin.get_ticker('bsv_krw')
    arr = [result_btc, result_xrp, result_auto, result_etc, result_trx, result_bch, result_bsv]
    if len(arr) != 0:
        for item in arr:
            d = datetime.fromtimestamp(int(item['timestamp']))
            item['year'] = d.year
            item['month'] = d.month
            item['day'] = d.day
            item['hour'] = d.hour
            item['minute'] = d.minute
            item['second'] = d.second
        mongodb.insert_items(arr)