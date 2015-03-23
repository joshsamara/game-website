# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='group',
            field=models.ForeignKey(blank=True, to='core.Group', null=True),
            preserve_default=True,
        ),
    ]
