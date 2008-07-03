#!/usr/bin/env python
from django.template import Library
from pylogs.blog.models import Post
from pylogs.blog.templatetags.themes import theme_template_url

register = Library()
def get_tagged_posts(tags,number_of_posts,exclude_id = None):
    '''get tagged related posts'''
    posts = []
    for tag in tags:        
        if len(posts) < number_of_posts:
            for p in tag.post_set.filter(post_type__iexact='post')[:number_of_posts-len(posts)]:
                if (not exclude_id or p.id != exclude_id) and p not in posts:
                    posts.append(p)                   
        else:
            break    
    return {'posts':posts}
register.inclusion_tag(theme_template_url() + '/blog/tags/related_posts.html')(get_tagged_posts)