"""All database models for this application."""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from stdimage.models import StdImageField
from django.core.urlresolvers import reverse
from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    """
    User for this site.

    Requires only an email and password.
    """

    GENDER_CHOICES = (('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Other'),)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin '
                                   'site.')
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              blank=True)
    public = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

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
