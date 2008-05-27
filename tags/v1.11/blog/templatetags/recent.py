#coding=utf-8
from django.template import Library
from pylogs.blog.models import Post,Comments
from pylogs.blog.templatetags.themes import theme_template_url

register = Library()
def get_latest_posts(context):
    '''
    get the top nav menus
    '''
    posts = Post.objects.filter(post_type__exact='post')[:5]    
    return {'posts':posts}
    #return AllCategoriesNode(cats)
register.inclusion_tag(theme_template_url() + '/blog/tags/recent_posts.html', 
                        takes_context=True)(get_latest_posts)

def get_popular_posts(context):
    '''
    get the top 5 Popular posts
    '''
    posts = Post.objects.filter(post_type__exact='post').order_by('-hits')[:5]    
    return {'posts':posts}
    #return AllCategoriesNode(cats)
register.inclusion_tag(theme_template_url() + '/blog/tags/recent_posts.html', 
                        takes_context=True)(get_popular_posts)

def get_latest_comments(context):
    '''get the top 5 comments'''
    comments = Comments.objects.filter(comment_approved__iexact='1')[:5]
    return {'comments':comments}
register.inclusion_tag(theme_template_url() + '/blog/tags/recent_comments.html', 
                        takes_context=True)(get_latest_comments)