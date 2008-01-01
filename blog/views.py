#coding=utf-8
from pylogs.blog.models import Post
from django.template import loader,Context
from django.utils import encoding
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response

def index(request,postid=0):
    postid=int(postid)
#    return HttpResponse(encoding.iri_to_uri('中国'))
    if postid==0:
        posts = Post.objects.all().exclude(post_type__iexact = 'page')[:5] #.values('id','title','pubdate')
        return render_to_response('blog/index.html',{'posts':posts})
    else:
        postInfo = get_object_or_404(Post,id__exact=postid)
        return process('blog/post.html',postInfo)
    
def post(request,postname=None,postid=0):
    '''get post by post name'''
    if postname:
        #get by postname
        postname = encoding.iri_to_uri(postname)
        post = get_object_or_404(Post,post_name__exact=postname,post_type__iexact='post')        
    elif int(postid)>0:
        #get by postid
        post = get_object_or_404(Post,id__exact=postid,post_type__iexact='post')
    if post:
        return process('blog/post.html',post)
    else:
        return HttpResponse(_('Sorry! This post not found!'))
    
    
def page(request,pagename):
    '''get page by page name'''
    if pagename:
        pagename = encoding.iri_to_uri(pagename)
        page = get_object_or_404(Post,post_name__exact=pagename,post_type__iexact='page')
        return process('blog/page.html',page)        
    else:
        return HttpResponse(_('Sorry! This page not found!'))
    
def dateposts(request,year,month,date):
    '''get posts by date'''
    if year:
        if month:
            if date:
                posts = get_list_or_404(Post,pubdate__year=year,pubdate__month=month,pubdate__day=date,post_type__iexact='post')
                return render_to_response('blog/datelist.html',{'year':year,'month':month,'day':date,'posts':posts})
            else:
                #month list
                posts = get_list_or_404(Post,pubdate__year=year,pubdate__month=month,post_type__iexact='post')
                return render_to_response('blog/datelist.html',{'year':year,'month':month,'posts':posts})
        else:
            #year list
            posts = get_list_or_404(Post,pubdate__year=year,post_type__iexact='post')
            return render_to_response('blog/datelist.html',{'year':year,'posts':posts})
                
def edit(request,postid=0):
    """
    编辑文章
    """
    postid=int(postid)
    if postid<=0:
        return render_to_response('blog/edit.html',None)
        #return HttpResponse('Sorry! No such article')
    else:
        postInfo = Post.objects.filedter(id__exact=postid)
        if postInfo:
            return process('blog/edit.html',postInfo[0])
        else:
            return HttpResponse('Sorry! This article not found!')

def save(request,postid=0):
    """
    保存文章
    """
    postid=int(postid)
    newtitle = request.POST['title']
    newcontent = request.POST['content']    
    if newtitle=='' or newcontent=='':
        return HttpResponse('Title and content can not be null.')
    if postid<=0:
        '''新建文章'''
        postInfo = Post(title=newtitle,content=newcontent,pubdate=currentTime())
        postInfo.save()
        
        postid= postInfo.id
    else:
        postInfo = Post.objects.filter(id__exact=postid)
        if postInfo:            
            postInfo[0].title = newtitle
            postInfo[0].content = newcontent
            postInfo[0].save()            
        else:
            return HttpResponse('Sorry! This article not found!')
    return HttpResponseRedirect("/blog/article/%s" % postid)
        
import time
def currentTime():
    '''
    取得当前时间(yyyy-MM-dd HH:mm:ss)格式
    '''
    n = time.localtime()
    return '%d-%d-%d %d:%d:%d' % (n.tm_year,n.tm_mon,n.tm_mday,n.tm_hour,n.tm_min,n.tm_sec)

import re
r = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
def process(template,post):
    """处理页面链接，并且将回车符转为<br>"""
    t = loader.get_template(template)    
    post.content = re.sub(r'[\n\r]+', '<br>', post.content)
    #c = Context({'pageid':page.id,'pagetitle':page.title, 'content':content,'categories':page.category.all()})
    c = Context({'post':post})    
    return HttpResponse(t.render(c))
    
    