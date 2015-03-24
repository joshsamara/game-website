from .utils import BaseTestCase as TestCase
from core.models import User


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
