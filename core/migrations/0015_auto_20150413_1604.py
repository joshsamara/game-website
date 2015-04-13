# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150413_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usernotification',
            old_name='link',
            new_name='redirect_url',
        ),
    ]
