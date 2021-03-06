from .utils import BaseTestCase as TestCase
from core.models import User, Group, GameTag, Game, MyFile, UserNotification, GroupInvitation
from django_dynamic_fixture import G
from django.core.urlresolvers import reverse


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

    def test_push_notification(self):
        user = G(User)
        self.assertNotExists(UserNotification, user=user)
        user.push_notification('123', 'abc')
        self.assertExists(UserNotification, user=user)


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

    def test_push_notification(self):
        user = G(User)
        group = G(Group)
        group.members = [user]
        self.assertNotExists(UserNotification, user=user)
        group.push_notification('123', 'abc')
        self.assertExists(UserNotification, user=user)


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

    def test_push_notification(self):
        game = G(Game)
        user = G(User)
        group = G(Group)
        group.members = [user]
        game.group = group
        self.assertNotExists(UserNotification, user=user)
        game.push_notification()
        self.assertExists(UserNotification, user=user)


class UserNotificationTestCase(TestCase):
    def test_link(self):
        notification = G(UserNotification)
        expected = reverse('core:profile:notifications',
                           kwargs={'notification_id': notification.pk})
        self.assertEqual(notification.link, expected)

    def test_unicode(self):
        notification = G(UserNotification, description="Abc")
        self.assertEqual(str(notification), "Abc")


class GroupInvitationTestCase(TestCase):
    def test_accept(self):
        user = G(User)
        group = G(Group)
        invite = G(GroupInvitation, user=user, group=group)
        self.assertNotIn(user, group.members.all())
        self.assertExists(GroupInvitation, user=user)
        invite.accept()
        self.assertIn(user, group.members.all())
        self.assertNotExists(GroupInvitation, user=user)

    def test_decline(self):
        user = G(User)
        group = G(Group)
        invite = G(GroupInvitation, user=user, group=group)
        self.assertNotIn(user, group.members.all())
        self.assertExists(GroupInvitation, user=user)
        invite.decline()
        self.assertNotIn(user, group.members.all())
        self.assertNotExists(GroupInvitation, user=user)

    def test_invite_create(self):
        user = G(User)
        group = G(Group)
        self.assertNotExists(GroupInvitation, user=user)
        GroupInvitation.create(group=group, user=user, inviting=True)
        self.assertExists(UserNotification, user=user)
        self.assertExists(GroupInvitation, user=user)

    def test_request_create(self):
        user = G(User)
        user2 = G(User)
        group = G(Group)
        group.members = [user2]
        self.assertNotExists(GroupInvitation, user=user)
        GroupInvitation.create(group=group, user=user, inviting=False)
        self.assertExists(UserNotification, user=user2)
        self.assertExists(GroupInvitation, user=user)

    def test_valid_user_invite(self):
        user = G(User)
        user2 = G(User)
        group = G(Group)
        group.members = [user2]
        invite = GroupInvitation.create(group=group, user=user, inviting=True)
        self.assertTrue(invite.valid_user(user))
        self.assertFalse(invite.valid_user(user2))

    def test_valid_user_request(self):
        user = G(User)
        user2 = G(User)
        group = G(Group)
        group.members = [user2]
        invite = GroupInvitation.create(group=group, user=user, inviting=False)
        self.assertTrue(invite.valid_user(user2))
        self.assertFalse(invite.valid_user(user))
