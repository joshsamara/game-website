# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'core', '0001_initial'), (b'core', '0002_auto_20150320_0150'), (b'core', '0003_remove_game_owner'), (b'core', '0004_auto_20150320_1822'), (b'core', '0005_auto_20150320_1826'), (b'core', '0006_auto_20150320_1836'), (b'core', '0002_auto_20150318_1928'), (b'core', '0007_merge'), (b'core', '0008_auto_20150321_2352'), (b'core', '0009_gamerating'), (b'core', '0010_auto_20150325_1358'), (b'core', '0011_auto_20150406_1529'), (b'core', '0012_auto_20150406_1611'), (b'core', '0011_game_featured'), (b'core', '0013_merge'), (b'core', '0014_auto_20150413_1351'), (b'core', '0015_auto_20150413_1604'), (b'core', '0016_usernotification_read'), (b'core', '0014_auto_20150413_1639'), (b'core', '0017_merge'), (b'core', '0014_auto_20150408_1930'), (b'core', '0015_game_game_file'), (b'core', '0016_auto_20150408_2004'), (b'core', '0018_merge'), (b'core', '0019_auto_20150422_2004'), (b'core', '0019_auto_20150415_1917'), (b'core', '0020_merge')]

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('birthday', models.DateField(null=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')])),
                ('public', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('link', models.URLField()),
                ('image', stdimage.models.StdImageField(upload_to=b'game_images')),
                ('description', models.TextField(max_length=5000)),
                ('date_published', models.DateField()),
                ('event_name', models.CharField(max_length=75)),
                ('genre', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='game',
            name='group',
            field=models.ForeignKey(blank=True, to='core.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='date_published',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
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
            field=models.ManyToManyField(to=b'core.GameTag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='game',
            name='genre',
        ),
        migrations.AlterField(
            model_name='game',
            name='event_name',
            field=models.CharField(default=b'', max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=stdimage.models.StdImageField(null=True, upload_to=b'game_images', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='game',
            name='link',
        ),
        migrations.AddField(
            model_name='game',
            name='game_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='GameRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(choices=[(0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5)])),
                ('game', models.ForeignKey(to='core.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='game',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'N/A', b'Prefer not to disclose'), (b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
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
        migrations.AddField(
            model_name='game',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('redirect_url', models.URLField()),
                ('description', models.CharField(max_length=256)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=True, help_text=b'Determines whether or not your profile is open to the public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=True, help_text=b'Determines whether or not your profile is open to the public'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='MyFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_file', models.FileField(null=True, upload_to=b'', blank=True)),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_file',
        ),
        migrations.AlterField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=True, help_text=b'Determines whether or not your profile is open to the public'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='game_file',
            field=models.ManyToManyField(to=b'core.MyFile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='group',
            field=models.ForeignKey(to='core.Group'),
            preserve_default=True,
        ),
    ]
