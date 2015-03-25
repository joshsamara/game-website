from django.contrib import admin
from core.models import Game, Group, GameTag, GameRating

# Register your models here.
admin.site.register(Game)
admin.site.register(Group)
admin.site.register(GameTag)
admin.site.register(GameRating)