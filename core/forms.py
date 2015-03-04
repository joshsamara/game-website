from django.forms import ModelForm
from core.models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__'