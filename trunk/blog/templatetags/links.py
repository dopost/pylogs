<<<<<<< HEAD
#coding=utf-8
from django.template import Library

from blog.models import Links
from blog.templatetags.themes import theme_template_url

register = Library()
def get_links(context):  
    links = Links.objects.all()
    return {'links':links}   
register.inclusion_tag(['%s/blog/tags/links.html' % theme_template_url(),
                        'blog/tags/links.html'],
                        takes_context=True)(get_links)
=======
#coding=utf-8
from django.template import Library

from blog.models import Links
from blog.templatetags.themes import theme_template_url

register = Library()
def get_links(context):  
    links = Links.objects.all()
    return {'links':links}   
register.inclusion_tag(['%s/blog/tags/links.html' % theme_template_url(),
                        'blog/tags/links.html'],
                        takes_context=True)(get_links)
>>>>>>> 1b1aba63e4e25c4d81cdc8ee168ba60582ceb029
