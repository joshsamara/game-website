# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_game_game_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myfile',
            old_name='file',
            new_name='game_file',
        ),
        migrations.AddField(
            model_name='myfile',
            name='name',
            field=models.CharField(default='sss', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='game_file',
            field=models.ManyToManyField(to='core.MyFile', null=True, blank=True),
            preserve_default=True,
        ),
    ]
