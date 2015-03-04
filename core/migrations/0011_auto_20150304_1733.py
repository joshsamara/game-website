# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150304_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='link',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
