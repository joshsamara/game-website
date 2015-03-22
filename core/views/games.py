from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import GameForm
from core.models import Game, Group
from django.views import generic

def main(request):
    games_list = Game.objects.all()
    return render(request, 'games/main.html', {
        'games_list': games_list
    })


def specific(request, game_id):
    game = Game.objects.get(pk=game_id)
    related_games = (game, game, game, game, game, game)
    return render(request, 'games/specific.html', {
        'game': game,
        'related_games': related_games,
    })


def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            return HttpResponseRedirect(reverse('core:games_specific', args=[game.id]))
    else:
        form = GameForm()
    return render(request, 'games/game_form.html', {
        'title': 'New Game',
        'heading': 'Creating New Game',
        'form': form
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
    return render(request, 'games/game_form.html', {
        'title': 'Edit Game',
        'heading': 'Currently Editing ' + selected_game.name,
        'form': form
    })
class GameSearch(generic.ListView):
    template_name='games/game_results.html'
    context_object_name = 'games'
    def get_queryset(self):
        game_name = self.kwargs['game_name']
        searchedGames = Game.objects.filter(name__contains=game_name)
        return searchedGames