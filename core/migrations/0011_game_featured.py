# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150325_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
