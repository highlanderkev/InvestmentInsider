# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a main controller for the insider application
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

# method for welcome page
def index():
    results = stocks = []
    count = page = limitby = 0
    items_per_page = 5
    query = ''
    if len(request.args):
        # this is for pagination
        page = request.args(0, cast=int)
        limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
        query = request.args(1)
        select_stocks = db.stock.security_name.like("%%%s%%" % query)
        select_symbols = db.stock.symbol.like("%%%s%%" % query)
        count = db((select_stocks)|(select_symbols)).count()
        stocks = db((select_stocks)|(select_symbols)).select(limitby=limitby)
    else:
        # flash welcome message
        response.flash = T("Welcome to Investment Insider!")
    # build the search form
    form = SQLFORM.factory(Field('search_query','string',requires=IS_NOT_EMPTY()), formstyle='divs', submit_button="Search")
    if form.process().accepted:
        page = 0
        limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
        stocks = db(db.stock).select()
        query = form.vars.search_query
        select_stocks = db.stock.security_name.like("%%%s%%" % query)
        select_symbols = db.stock.symbol.like("%%%s%%" % query)
        count = db((select_stocks)|(select_symbols)).count()
        stocks = db((select_stocks)|(select_symbols)).select(limitby=limitby)
        redirect(URL('default','index', args=[page, query]))
    return dict(form=form, stocks=stocks, count=count, page=page, items_per_page=items_per_page, query=query, limitby=limitby)

# method to see main stock page
def stock():
    stock = db.stock(request.args(0, cast=int)) or redirect(URL('default','index'))
    update(stock.symbol)
    response.flash = 'Reload Page to get updates.'
    stringname = stock.security_name.split('-')
    #response.title = stringname[0]
    #response.subtitle = stringname[1]
    market = db(db.stock_market.id==stock.market_id).select().first()
    db.post.stock_id.default = stock.id
    form = SQLFORM(db.post, fields=['body','outlook','link'], labels={'body':'Post','outlook':'Bull or Bear?','link':'Link'}, col3 = {'body':'(Required) 400 Characters Max','outlook':'(Required)','link':'(Optional) Requires http:// or https://'}, submit_button='Post').process()
    form.element(_type='submit')['_class']='btn btn-inverse'
    if form.accepted:
        if form.vars.link == 'http://' or form.vars.link == 'https://':
            db.post.update_or_insert(db.post.id==form.vars.id, link='')
        response.flash = 'New Post Added'
    elif form.errors:
        response.flash = 'Error Adding New Post'
    timespan = '1d'
    return dict(form=form, stock=stock, market=market, timespan=timespan)

# method for showing posts
def posts():
    stocksymbol = request.get_vars['stock']
    outlook = request.get_vars['outlook']
    stock = db(db.stock.symbol==stocksymbol).select().first()
    max_posts = 5
    posts = db((db.post.stock_id==stock.id)&(db.post.outlook==outlook)).select(orderby=~db.post.votes)
    return dict(stocksymbol=stocksymbol, outlook=outlook, posts=posts, max_posts=max_posts)

# method for loading chart
def chart():
    stocksymbol = request.get_vars['stock']
    timespan = request.get_vars['timespan']
    url = 'http://chart.yahoo.com/z?s=%s&t=%s' % (stocksymbol, timespan)
    return dict(url=url, stocksymbol=stocksymbol)

#method to vote up a post and show votes
def vote():
    post_id = request.args(0, cast=int)
    vote = request.args(1, cast=int)
    post = db(db.post.id==post_id).select().first()
    votes = post.votes
    voted = False
    if auth.user:
        prev_vote = db((db.vote.post_id==post_id)&(db.vote.voter==auth.user)).select().first()
        if prev_vote:
            if prev_vote.voted==True:
                # do nothing not allowed to vote
                voted = True
            else:
                voted = False
        else:
            if vote==1:
                votes = post.votes + 1
                post.update_record(votes=votes)
                voted = True
                db.vote.update_or_insert(voter=auth.user, post_id=post.id, voted=voted)
    return dict(votes=votes, post_id=post_id, voted=voted)

# method to run the stock ticker to see most up to date prices
def ticker():
    counter = request.now.second * 3
    ticker_items = 9
    limitby = (counter * ticker_items, (counter + 1) * ticker_items + 1)
    stock_ticks = db(db.stock).select(limitby=limitby)
    queue_realtime_update(stock_ticks)
    return dict(counter=counter, ticker_items=ticker_items, stock_ticks=stock_ticks)

# method for seeing user posts and other info
@auth.requires_login()
def userpage():
    user_id = request.args(0, cast=int)
    user = db(db.auth_user.id==user_id).select().first()
    posts = db(db.post.author==user_id).select()
    return dict(posts=posts, user=user)

# method for loading the most posted about stocks
def trending_stocks():
    stocksymbol = request.get_vars['stock']
    if stocksymbol:
        stock = db(db.stock.symbol==stocksymbol).select().first()
        redirect(URL('default','stock.html', args=stock.id))
    stocks = db(db.stock).select(db.stock.ALL)
    count = {}
    for stock in stocks:
        posts_count = db(db.post.stock_id==stock.id).count()
        if posts_count > 1:
            count[stock.symbol] = posts_count
    sortedcount = sort_counts(count)
    return dict(count=count, sortedcount=sortedcount)

# method for loading the most active users
def active_users():
    users = db(db.auth_user).select(db.auth_user.ALL)
    active = {}
    for user in users:
        posts_count = db(db.post.author==user).count()
        if posts_count > 1:
            active[user] = posts_count
    sortedcount = sort_counts(active)
    return dict(active=active, sortedcount=sortedcount)

# for user authentication
def user():
    return dict(form=auth())

# method to change user setttings
@auth.requires_login()
def settings():
    return dict()

# method for downloading files, currently disabled
'''
@cache.action()
def download():
    return response.download(request, db)
'''

# method for services, xml, json, rss, csv
def call():
    return service()

# method for access to data (SQL tables)
@auth.requires_signature()
def data():
    return dict(form=crud())
