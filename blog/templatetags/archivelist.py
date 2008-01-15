#!/usr/bin/env python
#coding=utf-8
from django.utils.translation import ugettext as _
from django.template import Library
from django.db import connection, transaction
register = Library()
def get_archivelist(context):
    '''
    get the month list which have posts
    ''' 
    cursor = connection.cursor()
    months = cursor.execute("select distinct strftime('%%Y/%%m',pubdate) as mon from blog_post order by mon desc")
    archive_months = []
    for mon in months:
        m = archives()
        m.link = "/" + mon[0] + "/"
        m.title = mon[0].replace('/',_(u'年'))
        m.title += _(u'月')
        archive_months.append(m)
    return {'archive_months':archive_months}

class archives():
    link = ''
    title = ''
    
register.inclusion_tag('blog/tags/archivelist.html', takes_context=True)(get_archivelist)
