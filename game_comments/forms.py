from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button
from crispy_forms.layout import Fieldset
from django_comments import CommentForm, Comment


class GameCommentForm(CommentForm):
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(GameCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # For some reason the form_id is not working. Leaving it as a reminder
        # to fix it at some point
        self.helper.form_id = 'comment-form'
        self.helper.layout = Layout(
            Fieldset(
                'Post Comment',
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
