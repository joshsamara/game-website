# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_id', models.IntegerField()),
                ('game_link', models.CharField(max_length=200)),
                ('game_image', models.ImageField(upload_to=b'')),
                ('game_description', models.CharField(max_length=5000)),
                ('game_date_published', models.DateField()),
                ('game_author_name', models.CharField(max_length=75)),
                ('game_event_name', models.CharField(max_length=75)),
                ('game_genre', models.CharField(max_length=50)),
                ('game_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
