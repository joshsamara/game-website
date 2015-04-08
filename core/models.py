"""All database models for this application."""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from stdimage.models import StdImageField
from django.core.urlresolvers import reverse

from core.managers import GameManager
from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User for this site.

    Requires only an email and password.
    """

    GENDER_CHOICES = (('', 'Prefer not to disclose'),
                      ('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Other'),)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin '
                                             'site.')
    date_joined = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1,
                              blank=True,
                              choices=GENDER_CHOICES)
    public = models.BooleanField(default=True,
                                 help_text='Determines whether or not your profile is open to the public')

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def get_name(self):
        """Return the name that should be displayed to the public"""
        if not self.public:
            return 'Anonymous'
        elif self.get_full_name():
            return self.get_full_name()
        else:
            return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


class Group(models.Model):
    """Groups that can consist of Users."""

    members = models.ManyToManyField(User)
    name = models.CharField(max_length=50)

    def get_games(self):
        games = Game.objects.filter(group=self)
        return games

    def get_absolute_url(self):
        """Detail page for a group."""
        return reverse('core:groups-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name


class GameTag(models.Model):
    """Tags to label Games."""

    value = models.CharField(max_length=50)

    def __unicode__(self):
        return self.value


class Game(models.Model):
    """Game object."""

    name = models.CharField(max_length=50)
    image = StdImageField(upload_to='game_images', null=True, blank=True,
                          variations={'thumbnail': {'width': 200, 'height': 200}})
    game_file = models.FileField(blank=True, null=True)
    description = models.TextField(max_length=5000)
    date_published = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, blank=True, null=True)
    event_name = models.CharField(max_length=75, blank=True, default='')
    tags = models.ManyToManyField(GameTag, null=True, blank=True)
    featured = models.BooleanField(default=False)

    objects = GameManager()

    @property
    def small_description(self):
        if len(self.description) > 300:
            return self.description[:300] + '...'
        else:
            return self.description

    @property
    def average_rating(self):
        ratings = zip(*self.gamerating_set.all().values_list('value'))
        if ratings:
            ratings = ratings[0]
            return sum(ratings) / len(ratings)
        else:
            return None

    @property
    def total_ratings(self):
        ratings = zip(*self.gamerating_set.all().values_list('value'))
        if len(ratings) != 0:
            return len(ratings[0])
        return 0

    def __unicode__(self):
        return self.name


class GameRating(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    value = models.FloatField(choices=(
        (.5, .5),
        (1, 1),
        (1.5, 1.5),
        (2, 2),
        (2.5, 2.5),
        (3, 3),
        (3.5, 3.5),
        (4, 4),
        (4.5, 4.5),
        (5, 5),
    ))
