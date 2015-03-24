from django.test import TestCase


class BaseViewTestCase(TestCase):
    def url(self, *args, **kwargs):
        raise NotImplementedError

    def assertLoginRequired(self, *args, **kwargs):
        self.client.logout()
        response = self.client.get(self.url(*args, **kwargs))
        self.assertEqual(response.status_code, 302)

    def assertNoLoginRequired(self, *args, **kwargs):
        self.client.logout()
        response = self.client.get(self.url(*args, **kwargs))
        self.assertEqual(response.status_code, 200)
