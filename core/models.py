from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    game_link = models.CharField(max_length=200)
    game_image = models.ImageField(null=True)
    game_description = models.CharField(max_length=5000)
    game_owner = models.ForeignKey(User)
    game_date_published = models.DateField()
    game_author_name = models.CharField(max_length=75)
    game_event_name = models.CharField(max_length=75)
    game_genre = models.CharField(max_length=50)