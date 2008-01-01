from django.conf.urls.defaults import *
from django.conf import settings
urlpatterns = patterns('',
    # Example:
    # (r'^pylogs/', include('pylogs.foo.urls')),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^admin/r/', include('django.conf.urls.shortcut')),
    (r'^$', 'pylogs.blog.views.index'),  
    #(r'^login/$','pylogs.login.login'),
    #(r'^logout/$','pylogs.login.logout'),  
    #(r'^blog/$','pylogs.blog.views.index'),   
    #(r'^article/(?P<postid>\d+)/$','pylogs.blog.views.index'),
    #(r'^article/new/$','pylogs.blog.views.edit'),
    (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postid>\d+)/$','pylogs.blog.views.post'),
    (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postname>\S+)/$','pylogs.blog.views.post'),
   
    #(r'^blog/article/edit/(?P<postid>\d+)/$','pylogs.blog.views.edit'),
    #(r'^blog/article/save/$','pylogs.blog.views.save'),
    #(r'^blog/article/save/(?P<postid>\d+)/$','pylogs.blog.views.save'),
    
    (r'^category/(?P<catid>\d+)/$','pylogs.blog.category_view.index'),
    (r'^category/(?P<catname>\S+)/$','pylogs.blog.category_view.index'),
    
    (r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$','pylogs.blog.views.dateposts'),
    (r'^(?P<pagename>\w+)/$','pylogs.blog.views.page'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_PATH}),
                
    
    #(r'handler404', 'django.views.generic.simple.direct_to_template',{'template':'error/404.html'}),
)
