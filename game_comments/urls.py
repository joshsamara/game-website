from django.conf.urls import url, patterns
from game_comments.views import game_comment_post

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # We'll use core as our default app, so we won't have a url prefix
    url('', game_comment_post, name='game_comment_post')
)
