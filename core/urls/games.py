__author__ = 'mark'

from django.conf.urls import patterns, url
from core.views import games
urlpatterns = patterns(
    '',
    url(r'^$', games.main, name='games_main'),
    url(r'^my_games$', games.my_games, name='my_games'),
    url(r'^new/$', games.new_game, name='games_new'),
    url(r'^(?P<game_id>\d+)/$', games.specific, name='games_specific'),
    url(r'^(?P<game_id>\d+)/edit/$', games.edit, name='games_edit'),
    url(r'^(?P<game_id>\d+)/ratings/$', games.rate_games, name='games_ratings'),
    url(r'^search/(?P<game_name>\w+)$', games.GameSearch.as_view(), name='game_search'),
)