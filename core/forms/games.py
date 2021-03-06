"""Forms for games."""
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Button, Fieldset
from django import forms
from django.forms import Textarea
from core.models import Game
from core.models import MyFile
from django_select2.widgets import Select2MultipleWidget
from crispy_forms.layout import Div


class GameForm(forms.ModelForm):
    """Form for game creation and editing."""
    my_game_file = forms.FileField(required=False)
    game_version = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Game
        exclude = ['owner', 'date_published']
        widgets = {
            'description': Textarea(attrs={'cols': 100, 'rows': 5}),
            'tags': Select2MultipleWidget(),
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
                'group',
                'description',
                HTML("""{% if form.image.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.image.value }}">
                {% endif %}"""),
                'tags',
                'image',
                'event_name',
                Div(
                    HTML('<p class="blockLabel">Upload a file for this game.</p>'),
                    'game_version',
                    'my_game_file',
                    HTML("""\
                    {% if game.game_file %}
                    <div class="top10">
                        <h2 class="files-header">Current Game Files</h2>
                        <ul class="list-group lead">
                            {% for file in game.game_file.all %}
                                <li class="list-group-item"><a href="{{file}}" download> {{file.name}}</a></li>
                            {% empty %}
                                <li class="list-group-item">No files found</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}"""),
                    css_class="form-upload",
                ),
            ),
            FormActions(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick='history.go(-1);', css_class="btn-default")
            )
        )

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)
        game.save()

        # Save our tags
        tags = self.cleaned_data.get('tags')
        if tags:
            game.tags = tags
            game.save()

        # Save the game files
        my_file = self.cleaned_data.get('my_game_file')
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
