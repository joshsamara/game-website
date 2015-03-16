from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import GameForm
from core.models import Game, Group


def specific(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'games/specific.html', {
        'game': game
    })


def main(request):
    games_list = Game.objects.all()
    return render(request, 'games/main.html', {
        'games_list': games_list
    })


def my_games(request):
    groups = Group.objects.filter(members__id=request.user.id)
    games_list = Game.objects.filter(group__in=groups)
    return render(request, 'games/main.html', {
        'games_list': games_list
    })


def edit(request, game_id):
    selected_game = Game.objects.get(pk=game_id)

    permission_to_edit = False
    for u in selected_game.group.members.all():
        if request.user.id == u.id:
            permission_to_edit = True

    if not permission_to_edit:
        return HttpResponse("You don't have permission to edit this game")

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=selected_game)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:games_specific', args=[game_id]))
    else:
        form = GameForm(instance=selected_game)
    return render(request, 'games/edit_game.html', {
        'game_id': game_id,
        'form': form
    })