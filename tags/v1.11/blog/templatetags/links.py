#coding=utf-8
from django.template import Library
from pylogs.blog.models import Links
from pylogs.blog.templatetags.themes import theme_template_url
register = Library()
def get_links(context):  
    links = Links.objects.all()
    return {'links':links}
   
register.inclusion_tag(theme_template_url()+ '/blog/tags/links.html', takes_context=True)(get_links)
