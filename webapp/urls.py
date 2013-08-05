from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',    
    # Our main views URL, see webapp.core.urls 
    url(r'^',           include('webapp.core.urls')),
    # API & API documentation urls 
    url(r'^api/',       include('webapp.api.urls')),
    url(r'^api-docs/',  include('rest_framework_docs.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/',     include(admin.site.urls)),
)