from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
	game_id = models.IntegerField()
	game_link = models.CharField(max_length=200)
	game_image = models.ImageField()
	game_description = models.charField()
	game_owner = models.ForeignKey(User)
	game_date_published = models.DateField()
	game_author_name = models.CharField(max_length = 75)
	game_event_name = models.CharField(max_length = 75)
	game_genre = models.CharField(max_length=50)