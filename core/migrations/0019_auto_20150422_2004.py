# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_file',
            field=models.ManyToManyField(to='core.MyFile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='group',
            field=models.ForeignKey(to='core.Group'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='myfile',
            name='name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
