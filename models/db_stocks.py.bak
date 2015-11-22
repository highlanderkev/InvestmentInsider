# coding: utf8
# db defintions and functions for Investment Insider

import urllib
import datetime
import operator

# CAUTION: This method is for running during down times due to its heavy use of the db
def run_all_updates():
    stocks = db(db.stock).select(db.stock.ALL)
    for stock in stocks:
        update(stock.symbol)

# method for updating in realtime (used with ticker tape to update)
def realtime_updates(stocks):
    for stock in stocks:
        last_price = get_last_trade_price(stock.symbol)
        change = get_change_realtime(stock.symbol)
        change_percent = get_change_percent_realtime(stock.symbol)
        db.stock.update_or_insert(db.stock.symbol==stock.symbol, last_trade_price=last_price, price_change=change, price_change_percent=change_percent)

# method to upate stock info
def update(symbol):
    last_price = get_last_trade_price(symbol)
    change = get_change(symbol)
    change_percent = get_change_percent(symbol)
    previous_close = get_previous_close(symbol)
    todays_range = get_todays_range(symbol)
    today_open = get_today_open(symbol)
    todays_low = get_todays_low(symbol)
    todays_high = get_todays_high(symbol)
    fif_week_high = get_52_week_high(symbol)
    fif_week_low = get_52_week_low(symbol)
    pe = get_pe(symbol)
    eps = get_eps(symbol)
    market_cap = get_market_cap(symbol)
    volume = get_volume(symbol)
    average_daily_volume = get_average_daily_volume(symbol)
    db.stock.update_or_insert(db.stock.symbol==symbol, last_trade_price=last_price, price_change=change, price_change_percent=change_percent, previous_close=previous_close, todays_range=todays_range, today_open=today_open, todays_low=todays_low, todays_high=todays_high, fif_week_high=fif_week_high, fif_week_low=fif_week_low, pe=pe, eps=eps, market_cap=market_cap, volume=volume, average_daily_volume=average_daily_volume)
    return dict(symbol=symbol)

# method for grabbing the chart from Yahoo Finance
def get_chart(symbol, timespan):
    url = 'http://chart.yahoo.com/z?s=%s&t=%s' % (symbol, timespan)
    chart = urllib.urlopen(url)
    return chart

# this is a method to get all stock symbols from the markets
# currently just NASDAQ
def get_allstocksymbols():
    list = get_stocks_nasdaq()
    nasdaq = db(db.stock_market.title=='NASDAQ').select().first()
    listing = []
    for x in range(1, (len(list)-2)):
        listing.append(list[x])
    return listing

# this is a method to update all current stock symbols from the markets
# currently just NASDAQ
def update_allstocksymbols():
    list = get_stocks_nasdaq()
    nasdaq = db(db.stock_market.title=='NASDAQ').select().first()
    for x in range(1, (len(list)-2)):
        db.stock.update_or_insert(db.stock.symbol==list[x][0], market_id=nasdaq.id, symbol=list[x][0], security_name=list[x][1], market_category=list[x][2], test_issue=list[x][3], financial_status=list[x][4], round_lot_size=list[x][5])

# method to query the ftp of nasdaq for all listed stocks
def get_stocks_nasdaq():
    page = urllib.urlopen('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt').read()
    parsedpage = page.split("\r\n")
    parsedstrings = []
    for string in parsedpage:
        parsedstrings.append(split_string(string))
    return parsedstrings

# splits the formatted strings from nasdaq into seperate strings ['example|example|example'] = ['example','example','example']
def split_string(string):
    parsedstock = string.split("|")
    return parsedstock

# utility method for finding trending stocks
def sort_counts(list):
    sorted_list = sorted(list.iteritems(), key=operator.itemgetter(1))
    sorted_list.reverse()
    return dict(sorted_list=sorted_list)

# database defintion for a stock market (Currently just NASDAQ)
db.define_table('stock_market',
                Field('title', 'string'))
db.stock_market.id.readable = db.stock_market.id.writable = False

# database defintion for a stock
db.define_table('stock',
                Field('market_id', 'reference stock_market'),
                Field('symbol', 'string'),
                Field('security_name', 'string'),
                Field('market_category', 'string'),
                Field('test_issue', 'string'),
                Field('financial_status', 'string'),
                Field('round_lot_size', 'string'),
                Field('last_trade_price', 'string'),
                Field('price_change', 'string'),
                Field('price_change_percent', 'string'),
                Field('previous_close', 'string'),
                Field('todays_range', 'string'),
                Field('today_open', 'string'),
                Field('todays_low', 'string'),
                Field('todays_high', 'string'),
                Field('fif_week_high', 'string'),
                Field('fif_week_low', 'string'),
                Field('market_cap', 'string'),
                Field('pe', 'string'),
                Field('eps', 'string'),
                Field('volume', 'string'),
                Field('average_daily_volume', 'string'))
db.stock.id.readable = db.stock.id.writable = False

# outlook can either be long or shot
OUTLOOK = ('bull (long)','bear (short)')

# database definition for a post about a stock
db.define_table('post',
                Field('stock_id','reference stock'),
                Field('author', 'reference auth_user', default=auth.user_id, writable=False),
                Field('body','text', requires=IS_NOT_EMPTY()),
                Field('link','string', IS_URL(mode='generic', allowed_schemes=['http','https']), default='http://'),
                Field('outlook', requires=IS_IN_SET(OUTLOOK)),
                Field('votes', 'integer', default=0))
db.post.id.readable = db.post.id.writable = False
db.post.body.requires = IS_LENGTH(500)

# database definition for a vote from a user
db.define_table('vote',
                Field('post_id', 'reference post'),
                Field('voter', 'reference auth_user'),
                Field('voted', 'boolean', default=False))
db.vote.id.readable = db.vote.id.writable = False
