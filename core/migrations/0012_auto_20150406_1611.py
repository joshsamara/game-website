# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150406_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='date_published',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=1, choices=[(b'', b'Prefer not to disclose'), (b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=False, help_text=b'Determines whether or not your profile is open to the public'),
            preserve_default=True,
        ),
    ]
