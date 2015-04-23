"""Game related views."""
import json
import random
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from core.forms import GameForm
from core.models import Game, Group, GameRating, User


def main(request):
    """Main page that lists all the games."""
    games_list = Game.objects.all()
    return render(request, 'games/all_games.html', {
        'games_list': games_list,
        'title': 'All Games'
    })


def specific(request, game_id):
    """Handle individual pages for games."""
    game = get_object_or_404(Game, id=game_id)

    related_games = Game.objects.filter(tags__in=game.tags.all).distinct().exclude(pk=game.id)
    return render(request, 'games/specific.html', {
        'game': game,
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
        'form': form,
    })


@login_required
def edit(request, game_id):
    """Page to edit a game with."""
    selected_game = Game.objects.get(pk=game_id)
    if not request.user.can_edit_game(selected_game):
            return HttpResponseRedirect(reverse('core:games:specific', args=[game_id]))

    if request.method == 'DELETE':
        selected_game.delete()
        return JsonResponse({
            'url': reverse('core:home')
        })

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=selected_game)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:games:specific', args=[game_id]))
    else:
        form = GameForm(instance=selected_game)
    return render(request, 'games/edit_game.html', {
        'heading': 'Currently Editing ' + selected_game.name,
        'form': form,
        'game':selected_game,
    })


def my_games(request):
    """List the games that the user has permissions to edit."""
    groups = Group.objects.filter(members__id=request.user.id)
    games_list = Game.objects.filter(group__in=groups)
    return render(request, 'games/all_games.html', {
        'games_list': games_list,
        'title': 'My Games'
    })


def total_ratings(request, game_id):
    """Return the average rating and total number of ratings for a given game."""
    if request.method == 'GET':
        game = Game.objects.get(pk=game_id)
        response = {
            'total_ratings': game.total_ratings,
            'avg_rating': game.average_rating
        }
        return JsonResponse(response)


def rate_games(request, game_id):
    """Add/update/delete a game rating."""
    if request.user.is_authenticated():

        if request.method == 'PUT':
            data = json.loads(request.body)
            response = add_or_update_rating(game_id, request.user.id, data['value'])
            return HttpResponse(status=response)

        if request.method == 'GET':
            try:
                rating = GameRating.objects.get(user=request.user, game__pk=game_id)
                value = rating.value
            except ObjectDoesNotExist:
                value = 0
            response = {
                'value': value
            }
            return JsonResponse(response)

        if request.method == 'DELETE':
            try:
                current_rating = GameRating.objects.get(user=request.user, game__pk=game_id)
                current_rating.delete()
                return HttpResponse(status=204)
            except ObjectDoesNotExist:
                return HttpResponse(status=404)
        return HttpResponse(status=405)

    else:
        return HttpResponse('Unauthorized', status=401)


def add_or_update_rating(game_id, user_id, value):
    """Update a user's rating on a game, or create it if it doesn't exist.

    Note that this function has no sort of authentication or security on it and should
    only be used when the information given is already verified
    Returns 200 if the rating was updated, or 201 if it was created
    """
    value += 0.0
    user = User.objects.get(pk=user_id)
    game = Game.objects.get(pk=game_id)
    try:
        current_rating = GameRating.objects.get(user=user, game=game)
        response = 204
    except ObjectDoesNotExist:
        current_rating = GameRating(user=user, game=game)
        response = 201
    current_rating.value = value
    current_rating.save()
    return response


class GameSearch(generic.ListView):
    """Handle searching of games."""

    template_name = 'games/all_games.html'
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


class GameAPI(generic.View):
    def _get_games(self, name, featured=False, top=False, recent=False):
        """
        Get games based on the arguments provided.

        Filter takes precedence in argument order.
        param:name: name to filter on
        param:featured: get featured games
        param:top: get top games
        param:recent: get recently uploaded games

        No name will grab 21 random games.
        """
        randomize = False
        if name:
            games = Game.objects.filter(name__icontains=name)
            max_count = 21
        elif featured:
            games = Game.objects.filter(featured=True)
            max_count = 3
        elif top:
            games = Game.objects.all_by_rating()
            max_count = 3
        elif recent:
            games = Game.objects.order_by('-date_published').all()
            max_count = 3
        else:
            games = Game.objects.all()
            max_count = 21
            randomize = True

        size = len(games)
        games = [(game.pk, game.name, str(game.image), game.description) for game in games]
        if randomize:
            return random.sample(games, min(size, max_count))
        else:
            return games[:min(size, max_count)]

    def get(self, request, *args, **kwargs):

        # Add quick url formattings for games, use a single reverse
        # search as reference
        reverse_template = reverse('core:games:specific',
                                   kwargs={'game_id': 1}).replace('/1/', '')

        def quick_reverse(game_id):
            """Reverse for a game in a faster way."""
            return reverse_template + '/%d/' % game_id

        # Get query params
        game_name = self.request.GET.get('term', '')
        featured = self.request.GET.get('featured')
        top = self.request.GET.get('top')
        recent = self.request.GET.get('recent')

        # Get list
        games = self._get_games(game_name, featured, top, recent)

        # Format our JSON response
        game_list = []

        # Format our data to be sent back to the JS
        media_url = settings.MEDIA_URL
        for pk, name, image, description in games:
            game_list.append({'name': name,
                              'has_image': bool(image),
                              'image': media_url + image,
                              'description': description,
                              'url': quick_reverse(pk)})

        return JsonResponse(game_list, safe=False)
