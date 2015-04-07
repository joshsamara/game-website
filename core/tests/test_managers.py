from .utils import BaseTestCase as TestCase
from core.models import User, Game, GameRating
from django_dynamic_fixture import G


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.manager = User.objects

    def test_create_user(self):
        self.assertFalse(self.manager.all().exists())
        email = 'test@email.com'
        password = 'testpass'
        self.manager.create_user(email, password)
        self.assertExists(User, email=email)
        self.assertFalse(User.objects.get(email=email).is_superuser)

    def test_create_super_user(self):
        self.assertFalse(self.manager.all().exists())
        email = 'test@email.com'
        password = 'testpass'
        self.manager.create_superuser(email, password)
        self.assertExists(User, email=email)
        self.assertTrue(User.objects.get(email=email).is_superuser)

    def test_create_user_invalid(self):
        self.assertFalse(self.manager.all().exists())
        email = None
        password = 'testpass'
        self.assertRaises(ValueError, self.manager.create_user, email, password)


class GameManagerTestCase(TestCase):
    def setUp(self):
        self.manager = Game.objects

    def test_order_rating(self):
        middle = G(Game)
        highest = G(Game)
        lowest = G(Game)
        none = G(Game)

        G(GameRating, game=highest, value=5)
        G(GameRating, game=highest, value=4)
        G(GameRating, game=highest, value=5)

        G(GameRating, game=middle, value=5)
        G(GameRating, game=middle, value=4)
        G(GameRating, game=middle, value=1)

        G(GameRating, game=lowest, value=3)
        G(GameRating, game=lowest, value=4)
        G(GameRating, game=lowest, value=1)

        game_list = self.manager.all_by_rating()

        self.assertEqual(len(game_list), 4)
        self.assertEqual(game_list[0], highest)
        self.assertEqual(game_list[1], middle)
        self.assertEqual(game_list[2], lowest)
        self.assertEqual(game_list[3], none)
