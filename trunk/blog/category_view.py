#coding=utf-8
from pylogs.blog.models import Category,Post
from pylogs.blog import models
from django.template import loader,Context
from django.utils import encoding
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response

def index(request,catname=None,catid=0):
    catid=int(catid)
    if catname:
        #get by cat name
        catname = encoding.iri_to_uri(catname)        
        catInfo = get_object_or_404(Category,enname__exact=catname)        
    elif catid > 0:       
        #get by id      
        catInfo = Category.objects.filter(id__exact=catid)        
    if catInfo:
            posts = Post.objects.filter(category__id__exact=catInfo.id,
                                        post_type__iexact = 'post',
                                        post_status__iexact = models.POST_STATUS[0][0])
            #posts = catInfo.posts_set.all()
            t = loader.get_template('blog/category.html')           
            c = Context({'catInfo':catInfo,'posts':posts})            
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Sorry! No such Category!')