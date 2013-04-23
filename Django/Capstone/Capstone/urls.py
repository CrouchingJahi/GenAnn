from django.conf.urls import patterns, include, url
# from django.contrib import admin

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'genedb.views.index'),
    url(r'^submit/$', 'genedb.views.submit'),
    url(r'^result/$', 'genedb.views.result'),
    url(r'^result/file/(\w+)', 'genedb.views.file'),
    
    # url(r'^admin/', include(admin.site.urls)),
)
