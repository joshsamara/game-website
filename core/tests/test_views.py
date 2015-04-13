from .utils import BaseViewTestCase as TestCase
from django_dynamic_fixture import G
from core.models import User, Group, Game, GameRating
from django.core.urlresolvers import reverse
from datetime import datetime
import json


class RegisterViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:register')

    def test_no_login_required(self):
        self.assertNoLoginRequired()

    def test_register_valid(self):
        self.assertNotExists(User, email='test@email.com')
        response = self.client.post(self.url(), {'email': 'test@email.com',
                                                 'password1': '123',
                                                 'password2': '123'})

        # Should redirect on success
        self.assertRedirects(response, reverse('core:home'))
        # Created user should exist
        self.assertExists(User, email='test@email.com')

    def test_register_invalid_email(self):
        response = self.client.post(self.url(), {'email': 'test',
                                                 'password1': '123',
                                                 'password2': '123'})
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        response = self.client.post(self.url(), {'email': '',
                                                 'password1': '123',
                                                 'password2': '123'})
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        G(User, email='test@test.test')
        response = self.client.post(self.url(), {'email': 'test@test.test',
                                                 'password1': '123',
                                                 'password2': '123'})
        self.assertFormError(response, 'form', 'email', 'A user with that email already exists.')

    def test_register_invalid_pass(self):
        response = self.client.post(self.url(), {'email': 'test@email.com',
                                                 'password1': '',
                                                 'password2': '123'})

        self.assertFormError(response, 'form', 'password1', 'This field is required.')
        response = self.client.post(self.url(), {'email': 'test@email.com',
                                                 'password1': '123',
                                                 'password2': ''})
        self.assertFormError(response, 'form', 'password2', 'This field is required.')
        response = self.client.post(self.url(), {'email': 'test@email.com',
                                                 'password1': '123',
                                                 'password2': '321'})
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")


class ProfileRedirectViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:profile:base')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_redirect(self):
        user = self.client.login()
        response = self.client.get(self.url())
        self.assertRedirects(response, reverse('core:profile:user-profile',
                                               kwargs={'pk': user.pk}))


class ProfileViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:profile:user-profile', kwargs=kwargs)

    def test_no_login_required(self):
        user = G(User)
        self.assertNoLoginRequired(pk=user.pk)


class UserGroupsViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:user-groups')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_get_queryset(self):
        # Setup a User in a group first
        user = self.client.login()
        group = G(Group)
        group.members.add(user)
        group.save()
        response = self.client.get(self.url())
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0], group)


class GroupsViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups')

    def test_no_login_required(self):
        self.assertNoLoginRequired()


class GroupJoinViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups-join', kwargs=kwargs)

    def test_login_required(self):
        group = G(Group)
        self.assertLoginRequired(pk=group.pk)

    def test_join_group(self):
        user = self.client.login()
        group = G(Group)
        self.assertNotIn(user, group.members.all())
        self.client.get(self.url(pk=group.pk))
        self.assertIn(user, group.members.all())


class GroupLeaveViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups-leave', kwargs=kwargs)

    def test_login_required(self):
        user = G(User)
        self.assertLoginRequired(pk=user.pk)

    def test_leave_group(self):
        user = self.client.login()
        group = G(Group)
        group.members.add(user)
        group.save()
        self.assertIn(user, group.members.all())
        self.client.get(self.url(pk=group.pk))
        self.assertNotIn(user, group.members.all())


class GroupCreateTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups-new')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_create_group(self):
        self.assertNotExists(Group, name='TestGroup')
        self.client.login()
        response = self.client.post(self.url(), {'name': 'TestGroup'})
        # Created group should exist
        self.assertExists(Group, name='TestGroup')
        group = Group.objects.get(name='TestGroup')
        # Should redirect on success
        self.assertRedirects(response, reverse('core:groups-detail',
                                               kwargs={'pk': group.pk}))

    def test_create_invalid_group(self):
        self.assertNotExists(Group, name='TestGroup')
        self.client.login()
        response = self.client.post(self.url(), {'name': ''})
        self.assertFormError(response, 'form', 'name', 'This field is required.')


class GameMainTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:main')

    def test_no_login_required(self):
        self.assertNoLoginRequired()


class MyGamesTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:my_games')

    def test_no_login_required(self):
        self.assertNoLoginRequired()


class NewGameTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:new')

    def test_no_login_required(self):
        self.assertNoLoginRequired()

    def test_create_game(self):
        self.assertNotExists(Game, name='test')
        response = self.client.post(self.url(), {'name': 'test',
                                                 'description': 'desc'})

        self.assertExists(Game, name='test')
        game = Game.objects.get(name='test')
        # Should redirect on success
        self.assertRedirects(response, reverse('core:games:specific',
                                               kwargs={'game_id': game.id}))

    def test_create_invalid_game(self):
        self.assertNotExists(Game, name='test')
        response = self.client.post(self.url(), {'name': '',
                                                 'description': 'desc'})

        self.assertFormError(response, 'form', 'name', 'This field is required.')
        response = self.client.post(self.url(), {'name': 'test'})
        self.assertFormError(response, 'form', 'description', 'This field is required.')


class GameSpecificTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:specific', kwargs=kwargs)

    def test_no_login_required(self):
        game = G(Game)
        user = G(User)
        G(GameRating, user=user, game=game)
        self.assertNoLoginRequired(game_id=game.id)


class GameEditTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:edit', kwargs=kwargs)

    def test_login_required(self):
        game = G(Game)
        self.assertLoginRequired(game_id=game.id)

    def test_unable_to_edit(self):
        self.client.login()
        game = G(Game, name="old")
        response = self.client.post(self.url(game_id=game.id), {'name': 'new',
                                                                'description': 'desc'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Game.objects.get(id=game.id).name, "old")

    def test_edit(self):
        # Setup a game that the user can edit
        user = self.client.login()
        game = G(Game, name="old")
        group = G(Group)
        game.group = group
        group.members.add(user)
        game.save()
        group.save()
        self.assertNotExists(Game, name="new")
        # Edit the game
        response = self.client.post(self.url(game_id=game.id), {'name': 'new',
                                                                'description': 'desc'})
        self.assertRedirects(response, reverse('core:games:specific',
                                               kwargs={'game_id': game.id}))
        self.assertEqual(Game.objects.get(id=game.id).name, "new")

    def test_edit_form(self):
        # Setup a game that the user can edit
        user = self.client.login()
        game = G(Game, name="old")
        group = G(Group)
        game.group = group
        group.members.add(user)
        game.save()
        group.save()
        # Go to edit page
        response = self.client.get(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('games/game_form.html')

    def test_delete_game(self):
        # Setup a game that the user can edit
        user = self.client.login()
        game = G(Game)
        group = G(Group)
        game.group = group
        group.members.add(user)
        game.save()
        group.save()
        # Go to edit page
        response = self.client.delete(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 200)
        self.assertNotExists(Game, id=game.id)


class GameSearchTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:search')

    def test_no_login_required(self):
        self.assertNoLoginRequired()


class TotalRatingsTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:total_ratings', kwargs=kwargs)

    def test_no_login_required(self):
        game = G(Game)
        user = G(User)
        G(GameRating, user=user, game=game)
        self.assertNoLoginRequired(game_id=game.id)

    def test_works_no_ratings(self):
        game = G(Game)
        response = self.client.get(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 200)


class RateGamesTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:ratings', kwargs=kwargs)

    def test_login_required(self):
        game = G(Game)
        self.assertLoginRequired(game_id=game.id)

    def test_create_rating(self):
        game = G(Game)
        user = self.client.login()
        self.assertNotExists(GameRating, user=user)
        response = self.client.put(self.url(game_id=game.id),
                                   data=json.dumps({"value": 1}))
        self.assertEqual(response.status_code, 201)
        self.assertExists(GameRating, user=user)
        self.assertEqual(GameRating.objects.get().value, 1)

    def test_update_rating(self):
        game = G(Game)
        user = self.client.login()
        G(GameRating, user=user, game=game, value=1)
        response = self.client.put(self.url(game_id=game.id),
                                   data=json.dumps({"value": 4}))
        self.assertEqual(response.status_code, 204)
        self.assertExists(GameRating, user=user)
        self.assertEqual(GameRating.objects.get().value, 4)

    def test_get_rating(self):
        game = G(Game)
        user = self.client.login()
        G(GameRating, user=user, game=game, value=2)
        response = self.client.get(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["value"], 2)

    def test_get_nonexistant_rating(self):
        game = G(Game)
        self.client.login()
        response = self.client.get(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 200)

    def test_delete_rating(self):
        game = G(Game)
        user = self.client.login()
        rating = G(GameRating, user=user, game=game, value=2)
        response = self.client.delete(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 204)
        self.assertNotExists(GameRating, id=rating.id)

    def test_delete_nonexistant_rating(self):
        game = G(Game)
        self.client.login()
        response = self.client.delete(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        game = G(Game)
        self.client.login()
        response = self.client.post(self.url(game_id=game.id))
        self.assertEqual(response.status_code, 405)


class GamesAPITestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:api')

    def test_no_login_required(self):
        self.assertNoLoginRequired()

    def test_get_name(self):
        g1 = G(Game, name='hello')

        # Make a second non-featured game
        G(Game, name='bye')
        response = self.client.get(self.url(), {'term': 'hel'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], g1.name)

    def test_get_featured(self):
        g1 = G(Game, featured=True)

        # Make a second non-featured game
        G(Game, featured=False)
        response = self.client.get(self.url(), {'featured': True})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], g1.name)

    def test_get_top_rated(self):
        g1 = G(Game)
        G(GameRating, game=g1, value=5)

        # Make a second lower-rated game
        g2 = G(Game)
        G(GameRating, game=g2, value=1)

        response = self.client.get(self.url(), {'top': True})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], g1.name)
        self.assertEqual(response_data[1]['name'], g2.name)

    def test_get_recent(self):
        # Game 1 will be older
        g1 = G(Game)
        g1.date_published = datetime(2013, 5, 2)
        g1.save()

        g2 = G(Game)

        response = self.client.get(self.url(), {'recent': True})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], g2.name)
        self.assertEqual(response_data[1]['name'], g1.name)


class EditProfileViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:profile:edit')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_get_logged_in(self):
        self.client.login()
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)

    def test_edit_valid(self):
        # Setup a basic user
        user = self.client.login()
        user.first_name = ""
        user.last_name = ""
        user.gender = ""
        user.public = False
        user.save()

        # Update the user
        response = self.client.post(self.url(), {'first_name': 'test_first',
                                                 'last_name': 'test_last',
                                                 'gender': 'M',
                                                 'public': True})
        # Should redirect on success
        redirect_url = reverse('core:profile:base')
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=302)

        # Have to re-get the updated users
        user = User.objects.get(pk=user.pk)

        # Make sure we updated
        self.assertEqual(user.first_name, 'test_first')
        self.assertEqual(user.last_name, 'test_last')
        self.assertEqual(user.gender, 'M')
        self.assertEqual(user.public, True)


class ChangePasswordViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:profile:password_change')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_get_logged_in(self):
        self.client.login()
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)

    def test_change_valid(self):
        # Make a user
        username = "test@email.com"
        old_pw = '123'
        new_pw = '321'
        User.objects.create_user(username, password=old_pw)
        # Login as the user
        self.assertTrue(self.client.login(username=username, password=old_pw))
        # Change the user's password
        response = self.client.post(self.url(), {'old_password': old_pw,
                                                 'new_password1': new_pw,
                                                 'new_password2': new_pw})
        # Will redirect back to the profile page on success
        redirect_url = reverse('core:profile:base')
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=302)
        # Login with the new pw
        self.client.logout()
        self.assertFalse(self.client.login(username=username, password=old_pw))
        self.assertTrue(self.client.login(username=username, password=new_pw))

    def test_change_invalid(self):
        # Make a user
        username = "test@email.com"
        old_pw = '123'
        new_pw = '321'
        User.objects.create_user(username, password=old_pw)
        # Login as the user
        self.assertTrue(self.client.login(username=username, password=old_pw))
        # Enter differentv values for pw
        self.client.post(self.url(), {'old_password': old_pw,
                                      'new_password1': new_pw,
                                      'new_password2': 'different'})
        # This won't change password
        self.client.logout()
        self.assertFalse(self.client.login(username=username, password=new_pw))
        self.assertTrue(self.client.login(username=username, password=old_pw))
        # Enter wrong old password
        self.client.post(self.url(), {'old_password': 'not-old',
                                      'new_password1': new_pw,
                                      'new_password2': new_pw})
        # This won't change password
        self.client.logout()
        self.assertFalse(self.client.login(username=username, password=new_pw))
        self.assertTrue(self.client.login(username=username, password=old_pw))
