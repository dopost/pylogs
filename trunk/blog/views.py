#coding=utf-8
from django.utils.translation import ugettext as _
from pylogs.blog import models
from pylogs.blog.models import Post,Comments,Tags,Category
from pylogs.blog import blog_forms
from django.template import loader,Context
from django.utils import encoding
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response
from django.core.paginator import Paginator, InvalidPage
import re
from pylogs.utils import html,codehighlight
from pylogs.utils.email import new_comment_mail
from pylogs.blog.templatetags.themes import theme_template_url
#from cgi import escape

PAGE_SIZE = 10
LIST_TEMPLATE = theme_template_url()+ '/blog/list.html'
def index(request):
    '''site index view,show 10 latest post.'''
    pageid = int(request.GET.get('page', '1'))
    pagedPosts = Paginator(Post.objects.all().filter(post_type__iexact = 'post',
                                      post_status__iexact = models.POST_STATUS[0][0]),
                                 PAGE_SIZE)    
    return renderPaggedPosts(pageid,_('Home'),pagedPosts,True)

def post(request,postname=None,postid=0):
    '''get post by post name'''
    msg = None
    error = None
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
            if request.POST.get('comment_vcode','').lower() != request.session.get('vcode',''):
                error = 'The confirmation code you entered was incorrect!'
            else:  
                if form.is_valid():
                    comment = Comments(post = post,
                               comment_author=form.cleaned_data['comment_author'],
                               comment_author_email=form.cleaned_data['comment_author_email'],
                               comment_author_url=form.cleaned_data['comment_author_url'],
                               comment_author_IP=request.META['REMOTE_ADDR'],
                               comment_content = form.cleaned_data['comment_content'],
                               comment_approved=str(models.COMMENT_APPROVE_STATUS[0][0]),
                               comment_agent=request.META['HTTP_USER_AGENT'])
                    #escape the html code
                    #comment.comment_content = escape(comment.comment_content)
                    comment.save()
                    #send mail to admin
                    new_comment_mail(post.title,comment.comment_content)
                    msg = _('Comment post successful!')
                    form = blog_forms.CommentForm()
                    #return HttpResponseRedirect(post.get_absolute_url()+ '#comments')
        #if allow comment,show the comment form
        elif post.comment_status == models.POST_COMMENT_STATUS[0][0]:
            form = blog_forms.CommentForm()
        else:
            form = None
        if not request.session.get('post_hits_%s' % post.id):
            #update hits count
            post.hits = post.hits + 1
            post.save()
            request.session['post_hits_%s' % post.id] = True;
        #post.content = codehighlight.highlight_code(post.content)
        #post.content = html.htmlDecode(post.content)
        return render_to_response(theme_template_url()+ '/blog/post.html',
                                  {'post':post,'form':form,'msg':msg,'error':error},
                                  context_instance=RequestContext(request))
        #return process('blog/post.html',post)
    else:
        return HttpResponse(_('Sorry! This post not found!'))

def page(request,pagename):
    '''get page by page name'''
    msg = None
    error = None
    if pagename:
        pagename = encoding.iri_to_uri(pagename)
        page = get_object_or_404(Post,post_name__exact=pagename,post_type__iexact='page')
        #return process('blog/page.html',page)        
        #post back comment
        if request.method == 'POST':
            form = blog_forms.CommentForm(request.POST)
            if request.POST.get('comment_vcode','').lower() != request.session.get('vcode',''):
                error = 'The confirmation code you entered was incorrect!'
            else:                
                if form.is_valid():
                    comment = Comments(post = page,
                               comment_author=form.cleaned_data['comment_author'],
                               comment_author_email=form.cleaned_data['comment_author_email'],
                               comment_author_url=form.cleaned_data['comment_author_url'],
                               comment_author_IP=request.META['REMOTE_ADDR'],
                               comment_content = form.cleaned_data['comment_content'],
                               comment_approved=str(models.COMMENT_APPROVE_STATUS[0][0]),
                               comment_agent=request.META['HTTP_USER_AGENT'])
                    #escape the html code
                    #comment.comment_content = escape(comment.comment_content)
                    comment.save()
                    #send mail to admin
                    new_comment_mail(page.title,comment.comment_content)            
                    msg = _('Comment post successful!')
                    form = blog_forms.CommentForm()                
                    #return HttpResponseRedirect(page.get_page_url()+ '#comments')
        #if allow comment,show the comment form
        elif page.comment_status == models.POST_COMMENT_STATUS[0][0]:
            form = blog_forms.CommentForm()
        else:
            form = None
        if not request.session.get('post_hits_%s' % page.id):
            #update hits count
            page.hits = page.hits + 1
            page.save()
            request.session['post_hits_%s' % page.id] = True;
            
        #page.content = codehighlight.highlight_code(page.content)
        #page.content = html.htmlDecode(page.content)
        return render_to_response(theme_template_url()+ '/blog/page.html',
                                  {'post':page,'form':form,'msg':msg,'error':error},
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
                pagedPosts = Paginator(Post.objects.filter(
                    pubdate__year=year,
                    pubdate__month=month,
                    pubdate__day=date,
                    post_type__iexact='post',
                    post_status__iexact = models.POST_STATUS[0][0]),
                                             PAGE_SIZE)              
            else:
                #month list
                pagedPosts = Paginator(Post.objects.filter(pubdate__year=year,
                                        pubdate__month=month,
                                        post_type__iexact='post',
                                        post_status__iexact = models.POST_STATUS[0][0]),
                                             PAGE_SIZE)                
        else:
            #year list
            pagedPosts = Paginator(Post.objects.filter(pubdate__year=year,
                                    post_type__iexact='post',
                                    post_status__iexact = models.POST_STATUS[0][0]),
                                         PAGE_SIZE)
    pageTitle = '-'.join([str(year),str(month),str(date)])
    return renderPaggedPosts(pageid,pageTitle,pagedPosts)

def categoryView(request,catname=None,catid=0):
    'Return the posts in the category'
    catid=int(catid)   
    if catname:
        #get by cat name
        catname = encoding.iri_to_uri(catname)        
        catInfo = get_object_or_404(Category,enname__iexact=catname)        
    elif catid > 0:       
        #get by id      
        catInfo = get_object_or_404(Category,id__exact=catid)        
    if catInfo:
            pagedPosts = Paginator(Post.objects.filter(category__id__exact=catInfo.id,
                                        post_type__iexact = 'post',
                                        post_status__iexact = models.POST_STATUS[0][0]),PAGE_SIZE)
            pageid =  int(request.GET.get('page', '1'))       
            return renderPaggedPosts(pageid,catInfo.name,pagedPosts)           
    else:
        return HttpResponse(_('Sorry! No such Category!'))
    
def tags(request,tagname = None):
    '''get the tag related posts.'''
    msg = None
    if tagname:        
        tagname = encoding.iri_to_uri(tagname)        
        tag = get_object_or_404(Tags,slug__iexact=tagname)
        if tag:
            pageid = int(request.GET.get('page', '1'))
            pagedPosts = Paginator(tag.post_set.all().filter(post_type__iexact='post',
                                                                   post_status__iexact = models.POST_STATUS[0][0]),
                                    PAGE_SIZE)
        return renderPaggedPosts(pageid,tag.name,pagedPosts)
    else:
        #taglist page        
        max = Tags.objects.all().order_by('-reference_count')[:1]
        if max:
            max = max[0].reference_count
        else:
            max = 1        
        tags = get_list_or_404(Tags)
        for tag in tags:
            tag.reference_count = tag.reference_count * 10/max
        return render_to_response(theme_template_url()+ '/blog/tags.html',
                                  {'tags':tags,'max':max},
                                  context_instance=RequestContext(request))
    
    

def renderPaggedPosts(pageid,pageTitle,pagedPosts,showRecent = False):
    if pagedPosts.count <=0:
        raise Http404;
    currentPage = pagedPosts.page(pageid)
    data = {'pagetitle':pageTitle,'posts':currentPage.object_list}
    if currentPage.has_next():
        data["next_page"] = pageid +1
    if currentPage.has_previous():
        data["prev_page"] = pageid -1
    if showRecent:
        data["show_recent"] = showRecent
    c = Context(data)
    t = loader.get_template(LIST_TEMPLATE)
    return HttpResponse(t.render(c))
