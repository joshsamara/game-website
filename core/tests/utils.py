"""Utilities to be used in testing."""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from urlparse import urlparse
from faker import Faker
from core.models import User


class CustomClient(Client):

    """Client with a convenience login method."""

    def login(self, **credentials):
        """
        Login client with credentials.

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

    """Base test case for general purpose use."""

    def assertExists(self, model, **kwargs):
        """Assert that an object exists in the ORM given args for a query."""
        item_qs = model.objects.filter(**kwargs)
        self.assertEqual(len(item_qs), 1,
                         "Found %d objects with params %s on model %s"
                         % (len(item_qs), kwargs, model))

    def assertNotExists(self, model, **kwargs):
        """Assert that an object doesnt exist in the ORM."""
        item_qs = model.objects.filter(**kwargs)
        self.assertFalse(item_qs.exists(),
                         "Object(s) found for given params %s on model %s"
                         % (kwargs, model))


class BaseViewTestCase(BaseTestCase):

    """Test case with convenience methods in views."""

    # Only override client_class in the ViewTestCase
    # because only the view tests should use a client
    client_class = CustomClient
    _login_url = reverse('core:login')

    def url(self, *args, **kwargs):
        """Return the URL of the view, must override."""
        raise NotImplementedError

    def _assertLogin(self, required, *args, **kwargs):
        """Check whether a login is required for the view."""
        self.client.logout()
        response = self.client.get(self.url(*args, **kwargs))
        if required:
            self.assertIn(response.status_code, [302, 401, 403])
            if response.status_code == 302:
                # If it's redirecting, should be to the login page
                self.assertEqual(urlparse(response.get('Location')).path,
                                 self._login_url)
        else:
            self.assertEqual(response.status_code, 200)

    def assertLoginRequired(self, *args, **kwargs):
        """Assert login IS required."""
        self._assertLogin(True, *args, **kwargs)

    def assertNoLoginRequired(self, *args, **kwargs):
        """Assert login isn't required."""
        self._assertLogin(False, *args, **kwargs)
