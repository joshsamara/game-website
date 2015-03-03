# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_game_game_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_name',
            field=models.CharField(default='My Game Name', max_length=50),
            preserve_default=False,
        ),
    ]
