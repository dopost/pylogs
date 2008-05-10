from django import template
from django.template.defaultfilters import striptags
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
register = template.Library()
#def substring(value, l):
#    """
#    filter to have n chars from start of a string
#    """
#    
#    ending = (" ", ".", "\n", "!", "?", ",")
#
#    s=striptags(value)
#    if len(s) > l:
#        if s[0:l+1] not in ending:
#            c=""
#            i=l
#            while c!=" " and c!="\n" and i!=0:
#                i = i-1
#                c = s[i]
#        tmp = s[0:i]
#        if tmp=='':
#            return s[0:l] +  "..."
#        else:
#            return tmp + '...' 
#    else:
#        return force_unicode(s[0:l])
#register.filter(substring)

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
        return _('high')
    elif value == 1:
        return _('medium')
    else:
        return _('low')    
register.filter('priority_name',priority_name)
