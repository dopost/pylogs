#coding=utf-8
from django.template import Library
from pylogs.blog.models import Links

register = Library()
def get_links(context):  
    links = Links.objects.all()
    return {'links':links}
   
register.inclusion_tag('blog/tags/links.html', takes_context=True)(get_links)
