from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # We'll use core as our default app, so we won't have a url prefix
    url(r'^', include('core.urls.base', namespace="core")),
    url(r'^admin/', include(admin.site.urls), name="admin"),
    url(r'^comments/', include('game_comments.urls', namespace='game_comments')),
)
