#!/usr/bin/env python
#coding=utf-8
from django.template import Library
from pylogs.blog.models import Post
from django.db import connection
from django.utils.dateformat import format
from pylogs.blog.templatetags.themes import theme_template_url
class archive:
    link = ''
    title = ''
    
register = Library()
def get_archivelist(context):
    '''
    get the month list which have posts
    ''' 
    months = Post.objects.dates('pubdate','month',order='DESC')
    archive_months = []
    print len(months)
    for mon in months:
        m = archive()
        m.link = "/" + format(mon,'Y/m') + "/"
        m.title = format(mon,'b,Y')
        archive_months.append(m)
    print connection.queries[-1:]
    return {'archive_months':archive_months}
register.inclusion_tag(theme_template_url()+ '/blog/tags/archivelist.html', takes_context=True)(get_archivelist)

    

