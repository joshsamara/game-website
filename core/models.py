from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField


class Group(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    image = StdImageField(upload_to='game_images', variations={'thumbnail': {'width': 200, 'height': 200}})
    description = models.CharField(max_length=5000)
    owner = models.ForeignKey(User)
    date_published = models.DateField()
    group = models.ForeignKey(Group, null=True)
    event_name = models.CharField(max_length=75)
    genre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name