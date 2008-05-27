#coding=utf-8
from django.template import Library
from pylogs.blog.models import Category
from pylogs.blog.templatetags.themes import theme_template_url
register = Library()
def get_categories(context):  
    cats = Category.objects.all()
    return {'cats':cats}
   
register.inclusion_tag(theme_template_url()+ '/blog/tags/category.html', takes_context=True)(get_categories)
