from django.conf.urls import url, patterns, include
from game_comments import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # We'll use core as our default app, so we won't have a url prefix
    url(r'^post/', views.game_comment_post, name='post'),
    url('', include('django_comments.urls')),
)
