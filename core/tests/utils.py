from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from urlparse import urlparse
from faker import Faker
from core.models import User


class CustomClient(Client):
    """ Client with a convenience login method. """

    def login(self, **credentials):
        """ Login client with credentials.

        If no credentials are passed, will create a random user and login.
        If login fails, return false.
        If login succeeds:
            If a user was created, return the user
            Else, return True
        """
        user = True
        if not credentials:
            fake = Faker()
            email = fake.email()
            passwd = fake.password()
            user = User.objects.create_user(email, password=passwd)
            credentials = {'email': email, 'password': passwd}
        login_successful = super(CustomClient, self).login(**credentials)
        return login_successful and user


class BaseTestCase(TestCase):
    def assertExists(self, model, **kwargs):
        item_qs = model.objects.filter(**kwargs)
        self.assertEqual(len(item_qs), 1,
                         "Found %d objects with params %s on model %s"
                         % (len(item_qs), kwargs, model))

    def assertNotExists(self, model, **kwargs):
        item_qs = model.objects.filter(**kwargs)
        self.assertFalse(item_qs.exists(),
                         "Object(s) found for given params %s on model %s"
                         % (kwargs, model))


class BaseViewTestCase(BaseTestCase):
    """ Test case with convenience methods in views. """
    # Only override client_class in the ViewTestCase
    # because only the view tests should use a client
    client_class = CustomClient
    _login_url = reverse('core:login')

    def url(self, *args, **kwargs):
        raise NotImplementedError

    def _assertLogin(self, required, *args, **kwargs):
        self.client.logout()
        response = self.client.get(self.url(*args, **kwargs))
        if required:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(urlparse(response.get('Location')).path,
                             self._login_url)
        else:
            self.assertEqual(response.status_code, 200)

    def assertLoginRequired(self, *args, **kwargs):
        self._assertLogin(True, *args, **kwargs)

    def assertNoLoginRequired(self, *args, **kwargs):
        self._assertLogin(False, *args, **kwargs)
