from django.conf.urls import patterns, url
from core.views import Home, register, games

# Use this file to import all other url
urlpatterns = patterns(
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^register/$', register),
    url(r'^games/$', games.main),
    url(r'^games/(?P<game_id>\d+)/$', games.specific),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
