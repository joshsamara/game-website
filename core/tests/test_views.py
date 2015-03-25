from .utils import BaseViewTestCase as TestCase
from django_dynamic_fixture import G
from core.models import User, Group, Game
from django.core.urlresolvers import reverse


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
        return reverse('core:profile')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_redirect(self):
        user = self.client.login()
        response = self.client.get(self.url())
        self.assertRedirects(response, reverse('core:user-profile',
                                               kwargs={'pk': user.pk}))


class ProfileViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:user-profile', kwargs=kwargs)

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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response._container[0], "You don't have permission to edit this game")
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


class GameSearchTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('core:games:search')

    def test_no_login_required(self):
        self.assertNoLoginRequired()