from django import template
from django.template.defaultfilters import striptags
from django.utils.encoding import force_unicode

register = template.Library()
def substring(value, length):
    s=striptags(value)
    us = s #unicode(s, 'utf-8')
    gs = us.encode('gb2312')
    n = int(length)
    t = gs[:n]
    while True:
        try:
            unicode(t, 'gbk')
            break
        except:
            n -= 1
            t = gs[:n]
    t = t.decode('gb2312')
    if n< len(value):
        return t + '...'
    else:
        return t
register.filter(substring)

def priority_name(value):
    '''return priority name'''    
    if value == 2:      
        return 'high'
    elif value == 1:
        return 'medium'
    else:
        return 'low'    
register.filter('priority_name',priority_name)
