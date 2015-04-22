"""Forms for games."""
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Button, Fieldset
from django import forms
from django.forms import Textarea, CheckboxSelectMultiple
from core.models import Game
from core.models import MyFile


class GameForm(forms.ModelForm):
    """Form for game creation and editing."""
    my_game_file = forms.FileField(required=False)
    game_version = forms.IntegerField(min_value=1, required=False)

    class Meta:
        model = Game
        exclude = ['owner', 'date_published']
        widgets = {
            'description': Textarea(attrs={'cols': 100, 'rows': 15}),
            'tags': CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(GameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'game-form'
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
                'game_version',
                'my_game_file'
            ),
            FormActions(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick='history.go(-1);', css_class="btn-default")
            )
        )

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)
        game.save()
        my_file = self.cleaned_data['my_game_file']
        if my_file:
            my_file = MyFile(name=self.cleaned_data['game_version'], game_file=my_file)
            my_file.save()
            game.game_file.add(my_file)
        return game

    def clean_game_version(self):
        version = self.cleaned_data.get('game_version')
        game_file = self.cleaned_data.get('my_game_file')
        if game_file and not version:
            raise forms.ValidationError('Uploading a file requires a version.', code='invalid')
        elif not game_file and version:
            raise forms.ValidationError('Versioning requires a game file.', code='invalid')
        else:
            return version
