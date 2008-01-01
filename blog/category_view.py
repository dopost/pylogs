#coding=utf-8
from pylogs.blog.models import Category,Post
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response

def index(request,catname=None,catid=0):
    catid=int(catid)
    if catname:
        #get by cat name
        catInfo = get_object_or_404(Category,enname__exact=catname)        
    elif catid>0:       
        #get by id      
        catInfo = Category.objects.filter(id__exact=catid)        
    if catInfo:
            posts = Post.objects.filter(category__id__exact=catid,post_type__iexact = 'post')
            t = loader.get_template('blog/category.html')           
            c = Context({'catInfo':catInfo,'posts':posts})            
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Sorry! No such Category!')