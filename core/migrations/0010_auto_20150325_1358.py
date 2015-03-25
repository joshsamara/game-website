# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_gamerating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamerating',
            name='value',
            field=models.FloatField(choices=[(0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5)]),
            preserve_default=True,
        ),
    ]
