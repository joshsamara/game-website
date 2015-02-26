# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_game_game_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='game_author_name',
            new_name='author_name',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_date_published',
            new_name='date_published',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_event_name',
            new_name='event_name',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_genre',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_link',
            new_name='link',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_owner',
            new_name='owner',
        ),
    ]
