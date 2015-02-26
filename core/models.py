from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    image = models.ImageField(upload_to='game_images', null=True)
    description = models.CharField(max_length=5000)
    owner = models.ForeignKey(User)
    date_published = models.DateField()
    author_name = models.CharField(max_length=75)
    event_name = models.CharField(max_length=75)
    genre = models.CharField(max_length=50)
