from django_dynamic_fixture import G
from core.models import User, Group
from .utils import BaseViewTestCase
from django.core.urlresolvers import reverse


class RegisterViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:register')

    def test_no_login_required(self):
        self.assertNoLoginRequired()

    def test_register_valid(self):
        self.assertFalse(User.objects.filter(email='test@email.com').exists())
        response = self.client.post(self.url(), {'email': 'test@email.com',
                                                 'password1': '123',
                                                 'password2': '123'})

        # Should redirect on success
        self.assertRedirects(response, reverse('core:home'))
        # Created user should exist
        self.assertTrue(User.objects.filter(email='test@email.com').exists())

    def test_register_invalid_email(self):
        response = self.client.post(self.url(), {'email': 'test',
                                                 'password1': '123',
                                                 'password2': '123'})
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        response = self.client.post(self.url(), {'email': '',
                                                 'password1': '123',
                                                 'password2': '123'})
        self.assertFormError(response, 'form', 'email', 'This field is required.')

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


class ProfileRedirectViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:profile')

    def test_login_required(self):
        self.assertLoginRequired()


class ProfileViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:user-profile', kwargs=kwargs)

    def test_no_login_required(self):
        user = G(User)
        self.assertNoLoginRequired(pk=user.pk)


class UserGroupsViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:user-groups')

    def test_login_required(self):
        self.assertLoginRequired()


class GroupsViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups')

    def test_no_login_required(self):
        self.assertNoLoginRequired()


class GroupJoinViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups-join', kwargs=kwargs)

    def test_login_required(self):
        user = G(User)
        self.assertLoginRequired(pk=user.pk)


class GroupLeaveViewTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups-leave', kwargs=kwargs)

    def test_login_required(self):
        user = G(User)
        self.assertLoginRequired(pk=user.pk)


class GroupCreateTestCase(BaseViewTestCase):
    def url(self, *args, **kwargs):
        return reverse('core:groups-new')

    def test_login_required(self):
        self.assertLoginRequired()

    def test_create_group(self):
        self.assertFalse(Group.objects.filter(name='TestGroup').exists())
        self.client.login()
        response = self.client.post(self.url(), {'name': 'TestGroup'})
        # Created group should exist
        self.assertTrue(Group.objects.filter(name='TestGroup').exists())
        group = Group.objects.get(name='TestGroup')
        # Should redirect on success
        self.assertRedirects(response, reverse('core:groups-detail',
                                               kwargs={'pk': group.pk}))

    def test_create_invalid_group(self):
        self.assertFalse(Group.objects.filter(name='TestGroup').exists())
        self.client.login()
        response = self.client.post(self.url(), {'name': ''})
        self.assertFormError(response, 'form', 'name', 'This field is required.')
