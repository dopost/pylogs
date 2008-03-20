#coding=utf-8
from django.utils.translation import ugettext as _
from pylogs.blog import models
from pylogs.blog.models import Post,Comments
from pylogs.blog import blog_forms
from django.template import loader,Context
from django.utils import encoding
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response
from django.core.paginator import ObjectPaginator, InvalidPage
import re
from utils import html,codehighlight
from pylogs.blog.templatetags.themes import theme_template_url

PAGE_SIZE = 10
def index(request):
    '''site index view,show 10 latest post.'''
    posts = Post.objects.all().filter(post_type__iexact = 'post',
                                      post_status__iexact = models.POST_STATUS[0][0])[:10]
    for post in posts:
        post.content = html.htmlDecode(post.content)    
    return render_to_response(theme_template_url()+ '/blog/index.html',{'posts':posts})    
    
def post(request,postname=None,postid=0):
    '''get post by post name'''
    msg = None
    if postname:
        #get by postname        
        postname = encoding.iri_to_uri(postname)
        #return HttpResponse(postname)
        post = get_object_or_404(Post,post_name__iexact=postname,post_type__iexact='post')        
    elif int(postid)>0:
        #get by postid
        post = get_object_or_404(Post,id__exact=postid,post_type__iexact='post')
    if post:
        #post back comment
        if request.method == 'POST':
            form = blog_forms.CommentForm(request.POST)
            if form.is_valid():
                comment = Comments(post = post,
                           comment_author=form.cleaned_data['comment_author'],
                           comment_author_email=form.cleaned_data['comment_author_email'],
                           comment_author_url=form.cleaned_data['comment_author_url'],
                           comment_author_IP=request.META['REMOTE_ADDR'],
                           comment_content = form.cleaned_data['comment_content'],
                           comment_approved=str(models.COMMENT_APPROVE_STATUS[0][0]),
                           comment_agent=request.META['HTTP_USER_AGENT'])
                comment.save()
                msg = _('Comment post successful!')
                form = blog_forms.CommentForm()
                #return HttpResponseRedirect(post.get_absolute_url()+ '#comments')
        #if allow comment,show the comment form
        elif post.comment_status == models.POST_COMMENT_STATUS[0][0]:
            form = blog_forms.CommentForm()
        else:
            form = None
        #update hits count
        post.hits = post.hits + 1
        post.save()        
        post.content = codehighlight.highlight_code(post.content)
        post.content = html.htmlDecode(post.content)
        return render_to_response(theme_template_url()+ '/blog/post.html',
                                  {'post':post,'form':form,'msg':msg},
                                  context_instance=RequestContext(request))
        #return process('blog/post.html',post)
    else:
        return HttpResponse(_('Sorry! This post not found!'))

def page(request,pagename):
    '''get page by page name'''
    msg = None
    if pagename:
        pagename = encoding.iri_to_uri(pagename)
        page = get_object_or_404(Post,post_name__exact=pagename,post_type__iexact='page')
        #return process('blog/page.html',page)        
        #post back comment
        if request.method == 'POST':
            form = blog_forms.CommentForm(request.POST)
            if form.is_valid():
                comment = Comments(post = page,
                           comment_author=form.cleaned_data['comment_author'],
                           comment_author_email=form.cleaned_data['comment_author_email'],
                           comment_author_url=form.cleaned_data['comment_author_url'],
                           comment_author_IP=request.META['REMOTE_ADDR'],
                           comment_content = form.cleaned_data['comment_content'],
                           comment_approved=str(models.COMMENT_APPROVE_STATUS[0][0]),
                           comment_agent=request.META['HTTP_USER_AGENT'])
                comment.save()
                msg = _('Comment post successful!')
                form = blog_forms.CommentForm()                
                #return HttpResponseRedirect(page.get_page_url()+ '#comments')
        #if allow comment,show the comment form
        elif page.comment_status == models.POST_COMMENT_STATUS[0][0]:
            form = blog_forms.CommentForm()
        else:
            form = None
        #update hits count
        page.hits = page.hits + 1
        page.save()        
        page.content = codehighlight.highlight_code(page.content)
        page.content = html.htmlDecode(page.content)
        return render_to_response(theme_template_url()+ '/blog/page.html',
                                  {'post':page,'form':form,'msg':msg},
                                  context_instance=RequestContext(request))
        #return process('blog/post.html',post)
    else:
        return HttpResponse(_('Sorry! This page not found!'))
    
def dateposts(request,year,month,date):
    '''get posts by date'''
    
    pageid = int(request.GET.get('page', '1'))
    if year:
        year = int(year)    
        if month:
            month =int(month)    
            if date:
                date =int(date)
                pagedPosts = ObjectPaginator(Post.objects.filter(
                    pubdate__year=year,
                    pubdate__month=month,
                    pubdate__day=date,
                    post_type__iexact='post',
                    post_status__iexact = models.POST_STATUS[0][0]),
                                             PAGE_SIZE)              
            else:
                #month list
                pagedPosts = ObjectPaginator(Post.objects.filter(pubdate__year=year,
                                        pubdate__month=month,
                                        post_type__iexact='post',
                                        post_status__iexact = models.POST_STATUS[0][0]),
                                             PAGE_SIZE)                
        else:
            #year list
            pagedPosts = ObjectPaginator(Post.objects.filter(pubdate__year=year,
                                    post_type__iexact='post',
                                    post_status__iexact = models.POST_STATUS[0][0]),
                                         PAGE_SIZE)            
    #no posts
    if pagedPosts.hits <=0:
        raise Http404;
    data = {'year':year,'month':month,'day':date,'posts':pagedPosts.get_page(pageid-1)}
    if pagedPosts.has_next_page(pageid-1):
        data["next_page"] = pageid +1
    if pagedPosts.has_previous_page(pageid-1):
        data["prev_page"] = pageid -1
    c = Context(data)
    t = loader.get_template(theme_template_url()+ '/blog/datelist.html')
    return HttpResponse(t.render(c))

def edit(request,postid=0):
    """
    edit post
    """
    postid=int(postid)
    if postid<=0:
        return render_to_response(theme_template_url()+ '/blog/edit.html',None)
        #return HttpResponse('Sorry! No such article')
    else:
        postInfo = Post.objects.filedter(id__exact=postid)
        if postInfo:
            return process(theme_template_url()+ '/blog/edit.html',postInfo[0])
        else:
            return HttpResponse(_('Sorry! This post not found!'))

def save(request,postid=0):
    """
    save post
    """
    postid=int(postid)
    newtitle = request.POST['title']
    newcontent = request.POST['content']    
    if newtitle=='' or newcontent=='':
        return HttpResponse(_('Title and content can not be null.'))
    if postid<=0:
        '''create post'''
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
            return HttpResponse(_('Sorry! This post not found!'))
    return HttpResponseRedirect(theme_template_url()+ "/blog/article/%s" % postid)  
    