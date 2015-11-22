# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# method to format datetime
def get_dateday(datetimeobject):
    datestring = datetimeobject.strftime("%b %d, %Y")
    return datestring

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = ''
response.title = 'Investment Insider'
response.subtitle = get_dateday(request.now)

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Kevin Patrick Westropp <mail@kevinpatrickwestropp.com>'
response.meta.description = 'Discuss investment stragies and become an insider.'
response.meta.keywords = 'stock, investments, trading, opinions'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]
