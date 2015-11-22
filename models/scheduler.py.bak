# coding: utf8
# scheduler for Investment Insider

import datetime

# second db for running background tasks
db_background = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])

# import the scheduler for running tasks
from gluon.scheduler import Scheduler
scheduler = Scheduler(db_background)

# scheduler method to run the realtime_updates for the stock ticker
def queue_realtime_update(stocks):
    symbols = []
    for stock in stocks:
        symbols.append(stock.symbol)
    scheduler.queue_task('realtime_updates', pargs=[symbols], immediate=True, timeout=(request.now + datetime.timedelta(minutes=2)))

# scheduler method to run an update on a stock
def queue_update(symbol):
    scheduler.queue_task('update', pargs=[symbol], immediate=True, timeout=(request.now + datetime.timedelta(minutes=2)))

# scheduler method to update all known stock symbols
def queue_update_allstocksymbols():
    scheduler.queue_task('update_allstocksymbols', immediate=True, timeout=(request.now + datetime.timedelta(minutes=2)))
