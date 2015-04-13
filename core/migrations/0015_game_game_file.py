# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150408_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_file',
            field=models.ManyToManyField(to='core.MyFile'),
            preserve_default=True,
        ),
    ]
