"""Forms for games."""
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Button, Fieldset
from django.forms import ModelForm, Textarea
from core.models import Game


class GameForm(ModelForm):

    """Form for game creation and editing."""

    class Meta:
        model = Game
        exclude = ['owner', 'date_published']
        widgets = {
            'description': Textarea(attrs={'cols': 100, 'rows': 15})
        }

    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(GameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '{{ heading }}',
                'name',
                'description',
                HTML("""{% if form.image.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.image.value }}">
                {% endif %}"""),
                'image',
                'tags',
                'group',
                'event_name',
                'game_file'
            ),
            FormActions(
                Submit('save', 'Save'),
                Button('cancel', 'Cancel', onclick='history.go(-1);', css_class="btn-default")
            )
        )
