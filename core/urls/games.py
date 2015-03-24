from django.conf.urls import patterns, url
from core.views import games

urlpatterns = patterns(
    '',
    url(r'^$', games.main, name='main'),
    url(r'^my_games$', games.my_games, name='my_games'),
    url(r'^new/$', games.new_game, name='new'),
    url(r'^(?P<game_id>\d+)/$', games.specific, name='specific'),
    url(r'^(?P<game_id>\d+)/edit/$', games.edit, name='edit'),
    url(r'^search/$', games.GameSearch.as_view(), name='search'),
)
