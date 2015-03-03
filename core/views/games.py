from django.shortcuts import render
from core.models import Game


def specific(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'games/games_specific.html', {
        'game': game
    })


def main(request):
    games_list = Game.objects.all()
    return render(request, 'games/games_main.html', {
        'games_list': games_list
    })