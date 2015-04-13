# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150413_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='read',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
