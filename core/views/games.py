from django.shortcuts import render
from core.models import Game


def main(request):
    latest_game_list = Game.objects.order_by('-id')[:5]
    return render(request, 'games/games_main.html', {
        'latest_game_list': latest_game_list
    })


def specific(request, game_id):
    return render(request, 'games/games_specific.html', {
        'game_id': game_id
    })


def create_game(request):
    return render(request, 'games/games_create.html')