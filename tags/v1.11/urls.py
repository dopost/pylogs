from django.conf.urls.defaults import *
from django.conf import settings
from pylogs.blog import feeds
from pylogs.blog.models import Post

# Info for feeds.
feed_dict = {    
    'rss': feeds.RssLatestPosts,
    'atom': feeds.AtomLatestPosts,
    }
info_dict = {    
    'queryset': Post.objects.all(),
    'date_field': 'pubdate',
}
urlpatterns = patterns('',
    # Example:
    # (r'^pylogs/', include('pylogs.foo.urls')),
    #(r'^(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year',info_dict),  
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^admin/r/', include('django.conf.urls.shortcut')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_PATH}),            
    (r'^utils/vcode/$', 'pylogs.utils.validatecode.get_validatecode_img'),
    #(r'handler404', 'django.views.generic.simple.direct_to_template',{'template':'error/404.html'}),
)
# url for todo
urlpatterns += patterns('',
                        (r'^todo/$', 'pylogs.todo.views.index'),
                        (r'^todo/task/add/', 'pylogs.todo.views.task_add'),
                        (r'^todo/task/done/','pylogs.todo.views.task_done'),
                        (r'^todo/task/undone/','pylogs.todo.views.task_undone'),
                        (r'^todo/task/delete/','pylogs.todo.views.task_del'),
                        (r'^todo/project/add/', 'pylogs.todo.views.project_add'),
                        (r'^todo/project/delete/', 'pylogs.todo.views.project_del'),
                        (r'^todo/project/change_type/', 'pylogs.todo.views.project_chg_type'),                        
                        )


## url for iplocater
#urlpatterns += patterns('',
#                        (r'^ip/$', 'django.views.generic.simple.direct_to_template',{'template':'iplocater/AjaxIp.html'}),
#                        (r'^ip/(?P<param_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$', 'pylogs.iplocater.views.searchIp'),                        
#                        )

# urls for blog
urlpatterns += patterns('',
                        
                        (r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',
                        {'feed_dict':feed_dict}),
                        (r'^$', 'pylogs.blog.views.index'),
                        #tags
                        (r'^tags/?(?P<tagname>.*)/$','pylogs.blog.views.tags'),
                        (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postid>\d+)/$','pylogs.blog.views.post'),
                        (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postname>[^/]+)/$','pylogs.blog.views.post'),
                        #category view
                        (r'^category/(?P<catid>\d+)/$','pylogs.blog.views.categoryView'),
                        (r'^category/(?P<catname>[^/]+)/$','pylogs.blog.views.categoryView'),                        
                        (r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$','pylogs.blog.views.dateposts'),
                        (r'^(?P<pagename>\w+)/$','pylogs.blog.views.page'),
                        )