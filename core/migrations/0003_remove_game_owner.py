# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150320_0150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='owner',
        ),
    ]
