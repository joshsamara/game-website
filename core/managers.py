"""Custom managers for models."""
from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager, Q
from django.utils import timezone


class UserManager(BaseUserManager):

    """Manager for our custom user model."""

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """Create and saves a User with the given email and password."""
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_superuser=is_superuser,
                          last_login=now, date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a non-permissioned user."""
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser."""
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class GameManager(Manager):
    def all_by_rating(self, descending=True):
        all_games = self.all()
        return sorted(all_games, key=lambda g: g.average_rating, reverse=descending)

    def search_by_term(self, term, annotated=True):
        games = self.filter(name__icontains=term)
        if games.count() < 5 or not annotated:
            from core.models import GameTag, Group
            tags = GameTag.objects.filter(value__icontains=term)
            groups = Group.objects.filter(name__icontains=term)

            query = Q(name__icontains=term) | Q(tags__in=tags) | Q(group__in=groups)
            games = self.filter(query).distinct()
        return games
