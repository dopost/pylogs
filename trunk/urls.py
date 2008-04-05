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
    
    #(r'handler404', 'django.views.generic.simple.direct_to_template',{'template':'error/404.html'}),
)
# url for iplocater
urlpatterns += patterns('',
                        (r'^ip/$', 'django.views.generic.simple.direct_to_template',{'template':'iplocater/AjaxIp.html'}),
                        (r'^ip/(?P<param_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$', 'pylogs.iplocater.views.searchIp'),                        
                        )


urlpatterns += patterns('',
                        (r'^pyadmin/', 'pylogs.pyadmin.views.index'),
                        )
# urls for blog
urlpatterns += patterns('',
                        
                        (r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',
                        {'feed_dict':feed_dict}),
                        (r'^$', 'pylogs.blog.views.index'),
                        #tags
                        (r'^tags/(?P<tagname>.*)/$','pylogs.blog.views.tags'),
                        (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postid>\d+)/$','pylogs.blog.views.post'),
                        (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postname>[^/]+)/$','pylogs.blog.views.post'),
                        #category view
                        (r'^category/(?P<catid>\d+)/$','pylogs.blog.views.categoryView'),
                        (r'^category/(?P<catname>[^/]+)/$','pylogs.blog.views.categoryView'),                        
                        (r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$','pylogs.blog.views.dateposts'),
                        (r'^(?P<pagename>\w+)/$','pylogs.blog.views.page'),
                        )