from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.core',
    url(r'^api/', include('apps.api.urls')),
    url(r'^api-docs/', include('rest_framework_docs'), name="Spending Stories API Documentation"),


)