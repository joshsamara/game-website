import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import GameForm
from core.models import Game, Group, GameRating, User
from django.views import generic


# Main page that lists all the games
def main(request):
    games_list = Game.objects.all()
    return render(request, 'games/main.html', {
        'games_list': games_list
    })


# Handles individual pages for games
def specific(request, game_id):
    game = Game.objects.get(pk=game_id)
    total_rating = 0
    ratings = GameRating.objects.filter(game=game)
    for rating in ratings:
        total_rating += rating.value
    if len(ratings) != 0:
        rating = total_rating / len(ratings)
    else:
        rating = 0

    related_games = Game.objects.filter(tags__in=game.tags.all).distinct().exclude(pk=game.id)
    return render(request, 'games/specific.html', {
        'game': game,
        'rating': rating,
        'related_games': related_games,
    })


# Form for creating a new game
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
            return HttpResponseRedirect(reverse('core:games_specific', args=[game_id]))
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
        'games_list': games_list
    })


def rate_games(request, game_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        add_or_update_rating(game_id, request.user.id, data['value'])
        return HttpResponse(status=204)
    if request.method == 'GET':
        rating = GameRating.objects.get(user=request.user, game__pk=game_id)
        response = {
            'value': rating.value
        }

    return HttpResponse(status=501)


# This will update a user's rating on a game, or create it if it doesn't exist
# Note that this function has no sort of authentication or security on it and should
# only be used when the information given is already verified
def add_or_update_rating(game_id, user_id, value):
    value += 0.0
    user = User.objects.get(pk=user_id)
    game = Game.objects.get(pk=game_id)
    try:
        current_rating = GameRating.objects.get(user=user, game=game)
    except ObjectDoesNotExist:
        current_rating = GameRating(user=user, game=game)
    current_rating.value = value
    current_rating.save()


# Handles searching of games
class GameSearch(generic.ListView):
    template_name = 'games/game_results.html'
    context_object_name = 'games'

    def get_queryset(self):
        game_name = self.kwargs['game_name']
        searched_games = Game.objects.filter(name__icontains=game_name)
        return searched_games