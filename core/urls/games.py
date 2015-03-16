__author__ = 'mark'

from django.conf.urls import patterns, url
from core.views import games

urlpatterns = patterns(
    '',
    url(r'^$', games.main, name='games_main'),
    url(r'^my_games$', games.my_games, name='my_games'),
    url(r'^(?P<game_id>\d+)/$', games.specific, name='games_specific'),
    url(r'^(?P<game_id>\d+)/edit/$', games.edit, name='games_edit'),
)