#coding=utf-8
from pylogs.blog.models import Category,Post
from pylogs.blog import models
from django.template import loader,Context
from django.utils import encoding
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import ObjectPaginator, InvalidPage
from pylogs.blog.templatetags.themes import theme_template_url
PAGE_SIZE = 10
def index(request,catname=None,catid=0):
    catid=int(catid)
    
    #return HttpResponse(pageid)
    if catname:
        #get by cat name
        catname = encoding.iri_to_uri(catname)        
        catInfo = get_object_or_404(Category,enname__iexact=catname)        
    elif catid > 0:       
        #get by id      
        catInfo = get_object_or_404(Category,id__exact=catid)        
    if catInfo:
            pagedPosts = ObjectPaginator(Post.objects.filter(category__id__exact=catInfo.id,
                                        post_type__iexact = 'post',
                                        post_status__iexact = models.POST_STATUS[0][0]),PAGE_SIZE)
            
            #posts = Post.objects.filter(category__id__exact=catInfo.id,
            #                            post_type__iexact = 'post',
            #                            post_status__iexact = models.POST_STATUS[0][0])
            #posts = catInfo.posts_set.all()
            t = loader.get_template(theme_template_url()+ '/blog/category.html')
            
            pageid =  int(request.GET.get('page', '1'))           
            data = {'catInfo':catInfo,'posts':pagedPosts.get_page(pageid-1)}
            if pagedPosts.has_next_page(pageid-1):
                data["next_page"] = pageid +1
            if pagedPosts.has_previous_page(pageid-1):
                data["prev_page"] = pageid -1
            c = Context(data)            
            return HttpResponse(t.render(c))
    else:
        return HttpResponse(_('Sorry! No such Category!'))