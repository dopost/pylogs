from django import template
from django.template.defaultfilters import striptags
from django.utils.encoding import force_unicode

register = template.Library()
def substring(value, l):
    """
    filter to have n chars from start of a string
    """
    
    ending = (" ", ".", "\n", "!", "?", ",")

    s=striptags(value)
    if len(s) > l:
        if s[0:l+1] not in ending:
            c=""
            i=l
            while c!=" " and c!="\n" and i!=0:
                i = i-1
                c = s[i]
        tmp = s[0:i]
        if tmp=='':
            return s[0:l] +  "..."
        else:
            return tmp + '...' 
    else:
        return force_unicode(s[0:l])
register.filter(substring)
