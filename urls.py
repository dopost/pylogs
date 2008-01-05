from django.conf.urls.defaults import *
from django.conf import settings
from pylogs.blog import feeds
# Info for feeds.
feed_dict = {    
    'rss': feeds.RssLatestPosts,
    'atom': feeds.AtomLatestPosts,
    }

urlpatterns = patterns('',
    # Example:
    # (r'^pylogs/', include('pylogs.foo.urls')),    
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^admin/r/', include('django.conf.urls.shortcut')),
    (r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',
            {'feed_dict':feed_dict}),
    (r'^$', 'pylogs.blog.views.index'),  
   
    (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postid>\d+)/$','pylogs.blog.views.post'),
    (r'^\d{4}/\d{1,2}/\d{1,2}/(?P<postname>[^/]+)/$','pylogs.blog.views.post'),
    
    (r'^category/(?P<catid>\d+)/$','pylogs.blog.category_view.index'),
    (r'^category/(?P<catname>\S+)/$','pylogs.blog.category_view.index'),
    
    (r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$','pylogs.blog.views.dateposts'),
    (r'^(?P<pagename>\w+)/$','pylogs.blog.views.page'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_PATH}),
                
    
    #(r'handler404', 'django.views.generic.simple.direct_to_template',{'template':'error/404.html'}),
)
