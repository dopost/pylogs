#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.utils.http import urlquote
from models import Path
import settings
from django.utils.http import urlquote
import os
import os.path
import re
from datetime import datetime
MEDIA_ROOT = settings.MEDIA_ROOT
ALLOW_FILE_TYPES = ('jpg','gif','png')
if settings.ALLOW_FILE_TYPES:
    ALLOW_FILE_TYPES = settings.ALLOW_FILE_TYPES
    
def index(request,p=None):
    if not request.user.is_authenticated():
        raise Http404()
    #render path list        
    dirs,files = [],[]
    #set default path root is MEDIA_ROOT/upload
    path = os.path.join(MEDIA_ROOT,'upload')
    dir_url_prefix = '/filemanager'
    file_url_prefix = '/media/upload'
    is_showup = False
    
    if p:
        print urlquote(p)
        is_showup = True
        path = os.path.join(path,p)
        file_url_prefix = file_url_prefix + '/' + p
        dir_url_prefix = dir_url_prefix + '/' + p
    
    #check the path is exists?
    if not os.path.exists(path):
        os.makedirs(path)   
    msg = ''
    #upload files to this path
    if request.method == 'POST':
        up_file = request.FILES.get('up_file')
        new_dirname = request.POST.get('newdir')
        if up_file:
            filename = up_file['filename']
            if not check_file_type(filename):
                return HttpResponse('<script>alert("%s");window.location.href = window.location.href;</script>'% 'Upload this file type is not allowed!')   
            filename = get_safe_filename(path,filename)
            print filename
            fd = open('%s/%s' % (path, filename), 'wb')   
            fd.write(up_file['content'])   
            fd.close()   
            msg = '上传成功，上传后的文件名为%s' % filename
            return HttpResponse('<script>alert("%s");window.location.href = window.location.href;</script>'% msg)   
        if new_dirname:
            #create new dir
            msg = ''
            new_dirname = os.path.join(path,new_dirname)
            try:
                os.mkdir(new_dirname)
                msg = '创建目录成功!'
            except:
                msg = '新建目录出现错误.'
            return HttpResponse('<script>alert("%s");window.location.href = window.location.href;</script>'% msg)   
    list_path(path,dirs,files,file_url_prefix,dir_url_prefix)
    current_loc = p
    for f in files:
        dirs.append(f)
    return render_to_response('filemanager/index.html',{'dirs':dirs,
                                                        'is_showup':is_showup,
                                                        'current_location':current_loc,
                                                        'msg':msg,
                                                        'allow_types':ALLOW_FILE_TYPES})

def get_safe_filename(path,filename):
    #get the safe filename on the server    
    if os.path.exists(os.path.join(path,filename)):
        r = re.compile(r'(\w+)\((\d+)\)$',re.I)
        filename_info = os.path.splitext(filename)
        m = r.match(filename_info[0])
        if m:
            f1 = m.groups(0)[0]
            f2 = int(m.groups(0)[1])
            filename =  '%s(%s)%s' % (f1,f2+1,filename_info[1])            
        else:
            filename = filename_info[0] + '(1)'+filename_info[1]
        return get_safe_filename(path,filename)
    else:        
        return filename
                
def list_path( path, dirs,files,file_url_prefix,dir_url_prefix):
    for fname in os.listdir(path):
        p = Path()
        p.name = fname
        fname = os.path.join(path,fname)
        #p.physical = os.path.normpath(fname)
        p.lastmodified = datetime.fromtimestamp(os.path.getmtime(fname))
        if os.path.isdir(fname):
            p.url = url_join(dir_url_prefix,p.name)
            p.is_dir = True
            dirs.append(p)            
        elif os.path.isfile(fname):
            p.url = url_join(file_url_prefix,p.name,True)
            p.size = os.path.getsize(fname)
            
            files.append(p)
            
def url_join(url1,url2,isfile = False):
    '''join a url'''
    url = '/'.join([url1,url2])
    if not isfile:
        url = url + '/'
    url = url.replace('//','/')
    return urlquote(url)

def check_file_type(filename):    
    nameinfo = os.path.splitext(filename)
    if len(nameinfo)< 2 or nameinfo[1][1:] not in ALLOW_FILE_TYPES:
        return False
    else:
        return True
   