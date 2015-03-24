from django.test import TestCase
from core.models import Group
from django_dynamic_fixture import G


class GroupTestCase(TestCase):
    def test_get_absolute_url(self):
        group = G(Group)
        group_id = group.id
        expected_url = '/groups/%d/' % group_id
        actual_url = group.get_absolute_url()
        self.assertEqual(expected_url, actual_url)
