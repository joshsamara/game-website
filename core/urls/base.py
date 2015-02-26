from django.conf.urls import patterns, url
from django.conf.urls.static import static
from core.views import Home, register, games

# Use this file to import all other url
from game_website import settings

urlpatterns = patterns(
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^games/(?P<game_id>\d+)/$', games.specific, name='games_specific'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Used to serve static media in a dev environment. Should be disabled in production
