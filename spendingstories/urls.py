from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    # Our main views URL, see spendingstories.core.urls 
    url(r'^$', redirect_to, {'url' : '/spending/'})
    url(r'^spending/', include('spendingstories.core.urls')),
    # API & API documentation urls 
    url(r'^api/', include('spendingstories.api.urls')),
    url(r'^api-docs/', include('rest_framework_docs.url')),

    url(r'^admin/', include(admin.site.urls)),
)