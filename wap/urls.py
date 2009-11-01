<<<<<<< HEAD
from django.conf.urls.defaults import *
urlpatterns = patterns('wap.views',                       
                       (r'^$','index'),
                       #tags
                       url(r'^tags/$','tags',name='wap_tags'),
                       url(r'^tags/(?P<tagname>.*)/$','tags',name='wap_tagname'),
                       url(r'^category/(?P<catid>\d+)/$','category',name="wap_category_id"),
                       url(r'^category/(?P<catname>[^/]+)/$','category',name="wap_category_name"),   
                       url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/(?P<postname>[^/]+)/$','post',name='wap_post_name'),
                       url(r'^(?P<pagename>\w+)/$','page',name='wap_page'),
=======
from django.conf.urls.defaults import *
urlpatterns = patterns('wap.views',                       
                       (r'^$','index'),
                       #tags
                       url(r'^tags/$','tags',name='wap_tags'),
                       url(r'^tags/(?P<tagname>.*)/$','tags',name='wap_tagname'),
                       url(r'^category/(?P<catid>\d+)/$','category',name="wap_category_id"),
                       url(r'^category/(?P<catname>[^/]+)/$','category',name="wap_category_name"),   
                       url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/(?P<postname>[^/]+)/$','post',name='wap_post_name'),
                       url(r'^(?P<pagename>\w+)/$','page',name='wap_page'),
>>>>>>> 1b1aba63e4e25c4d81cdc8ee168ba60582ceb029
)