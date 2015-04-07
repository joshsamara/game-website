"""Main URL file, include other URLs here."""
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from core.views import (Home, register, UserGroupsView,
                        GroupsView, GroupDetailView, GroupJoinView,
                        GroupLeaveView, GroupCreateView)

# Use this file to import all other url
from game_website import settings

urlpatterns = patterns(
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^games/', include('core.urls.games', namespace="games")),
    url(r'^register/$', register, name='register'),

    # TODO: Separate user urls out
    url(r'^profile/', include('core.urls.profile', namespace='profile')),

    url(r'^user/groups/$', UserGroupsView.as_view(), name='user-groups'),
    url(r'^groups/$', GroupsView.as_view(), name='groups'),
    url(r'^groups/(?P<pk>\d+)/$', GroupDetailView.as_view(), name='groups-detail'),
    url(r'^groups/(?P<pk>\d+)/join/$', GroupJoinView.as_view(), name='groups-join'),
    url(r'^groups/(?P<pk>\d+)/leave/$', GroupLeaveView.as_view(), name='groups-leave'),
    url(r'^groups/new/$', GroupCreateView.as_view(), name='groups-new'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': 'core:home'}, name='logout'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Used to serve static media in a dev environment. Should be disabled in production
