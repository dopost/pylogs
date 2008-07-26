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
                        (r'^admin/', include('django.contrib.admin.urls')),
                        (r'^admin/r/', include('django.conf.urls.shortcut')),                               
                        url(r'^utils/vcode/$', 'pylogs.utils.validatecode.get_validatecode_img',name='validate_code'),  
                        )

# url for static
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_PATH}),                    
                            )
# url for todo
urlpatterns += patterns('pylogs.todo.views',
                        url(r'^todo/$', 'index',name='todo'),
                        (r'^todo/task/add/', 'task_add'),
                        (r'^todo/task/done/','task_done'),
                        (r'^todo/task/undone/','task_undone'),
                        (r'^todo/task/delete/','task_del'),
                        (r'^todo/project/add/', 'project_add'),
                        (r'^todo/project/delete/', 'project_del'),
                        (r'^todo/project/change_type/', 'project_chg_type'),                        
                        )

# url for filemanager
urlpatterns += patterns('',                        
                        (r'^filemanager/(?P<p>.*)$', 'filemanager.views.index'),                        
                        )
#urls for feeds
urlpatterns += patterns('',
                        url(r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',
                        {'feed_dict':feed_dict},name='feeds'),
                        )
# urls for blog
urlpatterns += patterns('pylogs.blog.views',  
                        (r'^$', 'index'),
                        #tags
                        url(r'^tags/?(?P<tagname>.*)/$','tags',name='tags'),
                        url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/(?P<postid>\d+)/$','post',name='post_id'),
                        url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/(?P<postname>[^/]+)/$','post',name='post_name'),
                        #category view
                        url(r'^category/(?P<catid>\d+)/$','categoryView',name="category_id"),
                        url(r'^category/(?P<catname>[^/]+)/$','categoryView',name="category_name"),                        
                        (r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$','dateposts'),
                        url(r'^(?P<pagename>\w+)/$','page',name='page'),
                        )