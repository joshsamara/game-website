# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='link',
        ),
        migrations.AddField(
            model_name='game',
            name='game_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
