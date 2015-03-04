from django.forms import ModelForm, Textarea
from core.models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ['owner', 'date_published']
        widgets = {
            'description': Textarea(attrs={'cols': 100, 'rows': 15})
        }