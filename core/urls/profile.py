from django.conf.urls import patterns, url
from core.views import ProfileRedirectView, ProfileView, users

urlpatterns = patterns(
    '',
    url(r'^$', ProfileRedirectView.as_view(), name='base'),
    url(r'^(?P<pk>\d+)/$', ProfileView.as_view(), name='user-profile'),
    url(r'^edit/$', users.edit, name='edit'),
)