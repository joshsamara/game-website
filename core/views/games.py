from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from core.forms import GameForm
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


def edit(request, game_id):
    selected_game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=selected_game)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:games_specific', args=[game_id]))
    else:
        form = GameForm(instance=selected_game)
    return render(request, 'games/games_edit.html', {
        'game_id': game_id,
        'form': form
    })