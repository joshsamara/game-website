# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150320_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='genre',
        ),
        migrations.AlterField(
            model_name='game',
            name='event_name',
            field=models.CharField(default=b'', max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='group',
            field=models.ForeignKey(blank=True, to='core.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=stdimage.models.StdImageField(null=True, upload_to=b'game_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='tags',
            field=models.ManyToManyField(to='core.GameTag', null=True, blank=True),
            preserve_default=True,
        ), 
    ]
