# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=stdimage.models.StdImageField(upload_to=b'game_images'),
            preserve_default=True,
        ),
    ]
