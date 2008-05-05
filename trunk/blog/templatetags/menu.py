#coding=utf-8
from django.template import Library
from pylogs.blog.models import Post
from pylogs.blog.templatetags.themes import theme_template_url
from django.utils.translation import ugettext as _
register = Library()

def get_menus(context):
    '''
    get the top nav menus
    '''
    pages = Post.objects.filter(post_type__exact='page').order_by('menu_order')
    #static menu    
    homepage = Post(title=_('Home'),post_name='/')
    todo = Post(title=_('Todo'),post_name='todo')
    tags = Post(title=_('Tags'),post_name='tags')
    menus = [homepage,todo,tags] #{'/':'Home',}
    if pages:
        for page in pages:
            #menus[page.post_name] = page.title
            menus.append(page)
    return {'menus':menus}
    #return AllCategoriesNode(cats)
register.inclusion_tag(theme_template_url() + '/blog/tags/menu.html', 
                        takes_context=True)(get_menus)
