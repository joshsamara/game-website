# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=True, help_text=b'Determines whether or not your profile is open to the public'),
            preserve_default=True,
        ),
    ]
