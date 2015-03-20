# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_game_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='game',
            name='tags',
            field=models.ManyToManyField(to='core.GameTag'),
            preserve_default=True,
        ),
    ]
