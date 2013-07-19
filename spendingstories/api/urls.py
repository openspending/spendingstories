from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^spending/$', views.SpendingListView.as_view()),
    # url(r'^spending/compare$', views.SpendingListCompareView.as_view()),
    url(r'^spending/(?P<pk>[0-9]+)/$', views.SpendingDetails.as_view()),
    # url(r'^spending/(?P<pk>[0-9]+)/compare$', views.SpendingDetailsComparing.as_view()),
)
