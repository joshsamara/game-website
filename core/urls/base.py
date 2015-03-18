from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from core.views import Home, register, profile

# Use this file to import all other url
from game_website import settings

urlpatterns = patterns(
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^games/', include('core.urls.games')),
    url(r'^register/$', register, name='register'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': 'core:home'}, name='logout'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Used to serve static media in a dev environment. Should be disabled in production
