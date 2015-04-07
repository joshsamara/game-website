from django.core.management import call_command
from .utils import BaseTestCase as TestCase
from core.models import User, Group, Game, GameTag
import sys
from cStringIO import StringIO


class CommandsTestCase(TestCase):
    def test_makedata(self):
        "Test makedata command."

        # Want to hide STDOUT because the command prints
        sys.stdout = StringIO()

        # Some Asserts.
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(GameTag.objects.count(), 0)

        args = []
        opts = {}
        call_command('makedata', *args, **opts)

        # Some Asserts.
        self.assertEqual(User.objects.count(), 100)
        self.assertEqual(Group.objects.count(), 20)
        self.assertEqual(Game.objects.count(), 100)
        self.assertEqual(GameTag.objects.count(), 30)
