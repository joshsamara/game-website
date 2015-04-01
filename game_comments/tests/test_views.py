from .utils import BaseViewTestCase as TestCase
from django.core.urlresolvers import reverse


class PostCommentTestCase(TestCase):
    def url(self, *args, **kwargs):
        return reverse('game_comments:post', kwargs=kwargs)

    def test_login_required(self):
        self.assertLoginRequiredPost()
