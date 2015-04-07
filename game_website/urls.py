from django.conf.urls import include, url, patterns
from django.contrib import admin
import game_comments

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # We'll use core as our default app, so we won't have a url prefix
    url(r'^', include('core.urls.base', namespace="core")),
    url(r'^admin/', include(admin.site.urls), name="admin"),
    url(r'^comments/', include('game_comments.urls', namespace='game_comments')),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'registration/change_password.html'}, name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change', name='password_change_done')
)
