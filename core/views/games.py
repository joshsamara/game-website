import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import GameForm
from core.models import Game, Group, GameRating, User
from django.views import generic

"""Game related views."""


def main(request):
    """Main page that lists all the games."""
    games_list = Game.objects.all()
    return render(request, 'games/main.html', {
        'games_list': games_list,
        'title': 'All Games'
    })


def specific(request, game_id):
    """Handle individual pages for games."""
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


def new_game(request):
    """Form for creating a new game."""
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


def edit(request, game_id):
    """Page to edit a game with."""
    selected_game = Game.objects.get(pk=game_id)

    permission_to_edit = False
    if selected_game.group:
        for u in selected_game.group.members.all():
            if request.user.id == u.id:
                permission_to_edit = True

    if not permission_to_edit:
        return HttpResponse("You don't have permission to edit this game", status=403)

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


def my_games(request):
    """List the games that the user has permissions to edit."""
    groups = Group.objects.filter(members__id=request.user.id)
    games_list = Game.objects.filter(group__in=groups)
    return render(request, 'games/main.html', {
        'games_list': games_list,
        'title': 'My Games'
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


def add_or_update_rating(game_id, user_id, value):
    """ This will update a user's rating on a game, or create it if it doesn't exist
        Note that this function has no sort of authentication or security on it and should
        only be used when the information given is already verified"""
    value += 0.0
    user = User.objects.get(pk=user_id)
    game = Game.objects.get(pk=game_id)
    try:
        current_rating = GameRating.objects.get(user=user, game=game)
    except ObjectDoesNotExist:
        current_rating = GameRating(user=user, game=game)
    current_rating.value = value
    current_rating.save()


class GameSearch(generic.ListView):

    """Handle searching of games."""

    template_name = 'games/main.html'
    context_object_name = 'games'

    def get_queryset(self):
        """Search for games based on a provided term."""
        game_name = self.request.GET.get('term', '')
        searched_games = Game.objects.filter(name__icontains=game_name)
        return searched_games

    def get_context_data(self):
        """Set the list and the page title."""
        context = super(GameSearch, self).get_context_data()
        context['games_list'] = self.object_list
        context['title'] = 'Search Results'
        return context
