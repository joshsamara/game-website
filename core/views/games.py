from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import GameForm
from core.models import Game, Group
from django.views import generic


# Main page that lists all the games
def main(request):
    games_list = Game.objects.all()
    return render(request, 'games/main.html', {
        'games_list': games_list,
        'title': 'All Games'
    })


# Handles individual pages for games
def specific(request, game_id):
    game = Game.objects.get(pk=game_id)
    related_games = Game.objects.filter(tags__in=game.tags.all).distinct().exclude(pk=game.id)
    return render(request, 'games/specific.html', {
        'game': game,
        'related_games': related_games,
    })


# Form for creating a new game
def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            return HttpResponseRedirect(reverse('core:games:specific', args=[game.id]))
    else:
        form = GameForm()
    return render(request, 'games/game_form.html', {
        'title': 'New Game',
        'heading': 'Creating New Game',
        'form': form
    })


# Page to edit a game with
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
            return HttpResponseRedirect(reverse('core:games:specific', args=[game_id]))
    else:
        form = GameForm(instance=selected_game)
    return render(request, 'games/game_form.html', {
        'title': 'Edit Game',
        'heading': 'Currently Editing ' + selected_game.name,
        'form': form
    })


# Lists the games that the user has permissions to edit
def my_games(request):
    groups = Group.objects.filter(members__id=request.user.id)
    games_list = Game.objects.filter(group__in=groups)
    return render(request, 'games/main.html', {
        'games_list': games_list,
        'title': 'My Games'
    })


# Handles searching of games
class GameSearch(generic.ListView):
    template_name = 'games/main.html'
    context_object_name = 'games'

    def get_queryset(self):
        game_name = self.request.GET.get('term', '')
        searched_games = Game.objects.filter(name__icontains=game_name)
        return searched_games

    def get_context_data(self):
        context = super(GameSearch, self).get_context_data()
        context['games_list'] = self.object_list
        context['title'] = 'Search Results'
        return context
