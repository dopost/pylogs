#!/usr/bin/env python
#coding=utf-8
from django.template import Library
from django.db import connection, transaction
class archive:
    link = ''
    title = ''
    
register = Library()
def get_archivelist(context):
    '''
    get the month list which have posts
    ''' 
    cursor = connection.cursor()
    months = cursor.execute("select distinct strftime('%%Y/%%m',pubdate) as mon from blog_post order by mon desc")
    archive_months = []
    for mon in months:
        m = archive()
        m.link = "/" + mon[0] + "/"
        m.title = mon[0].replace('/',u'年')
        m.title += u'月'
        archive_months.append(m)
    return {'archive_months':archive_months}
register.inclusion_tag('blog/tags/archivelist.html', takes_context=True)(get_archivelist)

    

