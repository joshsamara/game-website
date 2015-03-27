"""Configuration for the admin site."""
from django.contrib import admin
from django_comments import Comment
from core.models import Game, Group, GameTag, User, GameRating

# Register your models here.
admin.site.register(User)
admin.site.register(Game)
admin.site.register(Group)
admin.site.register(GameTag)
admin.site.register(GameRating)
