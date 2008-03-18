from django.utils.translation import ugettext as _
from pylogs.blog import models
from pylogs.blog.models import Post,Comments
from django.template import loader,Context
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response
from pylogs.pyadmin.forms import PostForm
def index(request):
    postForm = PostForm()
    #return HttpResponse(postForm.as_table())
    return render_to_response('pyadmin/postform.html',{'form':postForm})