from .utils import BaseTestCase as TestCase
from core.models import User, Group, GameTag, Game, MyFile
from django_dynamic_fixture import G


class UserTestCase(TestCase):
    def test_get_full_name(self):
        user = G(User, first_name='test', last_name='last')
        expected = 'test last'
        self.assertEqual(expected, user.get_full_name())

    def test_get_short_name(self):
        user = G(User, first_name='test')
        self.assertEqual('test', user.get_short_name())

    def test_display_name_anon(self):
        user = G(User, first_name='test', last_name='last', public=False)
        expected = 'Anonymous'
        self.assertEqual(expected, user.display_name)

    def test_dsplay_name_first_last(self):
        user = G(User, first_name='test', last_name='last', public=True)
        expected = user.get_full_name()
        self.assertEqual(expected, user.display_name)

    def test_display_name_email(self):
        user = G(User, first_name='', last_name='', public=True)
        expected = user.email
        self.assertEqual(expected, user.display_name)


class GroupTestCase(TestCase):
    def test_get_absolute_url(self):
        group = G(Group)
        group_id = group.id
        expected_url = '/groups/%d/' % group_id
        actual_url = group.get_absolute_url()
        self.assertEqual(expected_url, actual_url)

    def test_unicode(self):
        group = G(Group, name='testgroup')
        self.assertEqual(str(group), 'testgroup')

    def test_get_games(self):
        group = G(Group, name='testgroup')
        self.assertEqual(list(group.get_games()), [])
        game = G(Game, group=group)
        self.assertEqual(list(group.get_games()), [game])


class GameTagTestCase(TestCase):
    def test_unicode(self):
        tag = G(GameTag, value='testtag')
        self.assertEqual(str(tag), 'testtag')


class GameTestCase(TestCase):
    def test_unicode(self):
        game = G(Game, name='testgame')
        my_file = G(MyFile, name='testFile')
        self.assertEqual(str(game), 'testgame')
        self.assertEqual(str(my_file), 'testFile')

    def test_small_description(self):
        game = G(Game, description='test')
        self.assertEqual(game.small_description, game.description)
        game.description = "x" * 5000
        game.save()
        self.assertEqual(game.small_description, ("x" * 300) + "...")
