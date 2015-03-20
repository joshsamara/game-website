from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from stdimage.models import StdImageField


class User(AbstractBaseUser, PermissionsMixin):
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
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name


class Group(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField()
    image = StdImageField(upload_to='game_images', variations={'thumbnail': {'width': 200, 'height': 200}})
    description = models.TextField(max_length=5000)
    date_published = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, null=True)
    event_name = models.CharField(max_length=75)
    genre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
