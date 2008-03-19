#!/usr/bin/env python
#coding=utf-8
from django.template import Library
from django.db import connection
from pylogs.blog.templatetags.themes import theme_template_url
class archive:
    link = ''
    title = ''
    
register = Library()
def get_archivelist(context):
    '''
    get the month list which have posts
    ''' 
    cursor = connection.cursor()
    #cursor.execute("select distinct strftime('%%Y/%%m',pubdate) as mon from blog_post order by mon desc")
    cursor.execute("select distinct DATE_FORMAT(pubdate,'%%Y/%%m') as mon from blog_post order by mon desc")
    months = cursor.fetchall()
    cursor.close()
    archive_months = []
    for mon in months:
        m = archive()
        m.link = "/" + mon[0] + "/"
        m.title = mon[0].replace('/',u'年')
        m.title += u'月'
        archive_months.append(m)    
    return {'archive_months':archive_months}
register.inclusion_tag(theme_template_url()+ '/blog/tags/archivelist.html', takes_context=True)(get_archivelist)

    

