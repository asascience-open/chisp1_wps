from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sciwps.views.home', name='home'),
    # url(r'^sciwps/', include('sciwps.foo.urls')),
    url(r'^wps/$', 'wps.views.wps'),
    url(r'^wps$', 'wps.views.wps'),
    url(r'^nlcs/$', 'nlcs.views.wps'),
    url(r'^nlcs$', 'nlcs.views.wps'),
    #url(r'^nlcs/reload/$', 'nlcs.views.reload'),
    url(r'^nlcs/reload$', 'nlcs.views.reload'),
    url(r'^outputs/(?P<filepath>.*)', 'nlcs.views.outputs'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
