#coding=utf-8
from django import template
from django.template import Library
from pylogs.blog.models import Category
from django.conf import settings

register = Library()
def get_categories(context):  
    cats = Category.objects.all()
    return {'cats':cats}
   
register.inclusion_tag('blog/tags/category.html', takes_context=True)(get_categories)
