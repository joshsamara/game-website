from .utils import BaseTestCase as TestCase
from core.models import User, Group
from django_dynamic_fixture import G


class UserTestCase(TestCase):
    def test_get_full_name(self):
        user = G(User, first_name='test', last_name='last')
        expected = 'test last'
        self.assertEqual(expected, user.get_full_name())

    def test_get_short_name(self):
        user = G(User, first_name='test')
        self.assertEqual('test', user.get_short_name())


class GroupTestCase(TestCase):
    def test_get_absolute_url(self):
        group = G(Group)
        group_id = group.id
        expected_url = '/groups/%d/' % group_id
        actual_url = group.get_absolute_url()
        self.assertEqual(expected_url, actual_url)

    def test_unicode(self):
        group = G(Group, name='test')
        self.assertEqual(str(group), 'test')
