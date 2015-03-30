from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button
from crispy_forms.layout import Fieldset
from django_comments import CommentForm


class GameCommentForm(CommentForm):
    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'comment-form'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'comment',
                'content_type',
                'object_pk',
                'timestamp',
                'security_hash',
            ),
            FormActions(
                Button('post', 'Post'),
            )
        )