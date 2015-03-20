# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150320_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='group',
            field=models.ForeignKey(default=1, to='core.Group'),
            preserve_default=False,
        ),
    ]
