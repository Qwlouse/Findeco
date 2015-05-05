# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import findeco.models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('key', models.CharField(default=findeco.models.generate_key, max_length=100)),
                ('key_valid_until', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('key', models.CharField(default=findeco.models.generate_key, max_length=100)),
                ('new_email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('key', models.CharField(default=findeco.models.generate_key, max_length=100)),
                ('key_valid_until', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Self-description')),
                ('is_verified_until', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0))),
                ('last_seen', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0))),
                ('verification_key', models.CharField(default=findeco.models.generate_key, max_length=64)),
                ('api_key', models.CharField(default=findeco.models.generate_api_key, max_length=16)),
                ('wants_mail_notification', models.BooleanField(default=False)),
                ('help_enabled', models.BooleanField(default=True)),
                ('preferred_language', models.CharField(default='', max_length=20)),
                ('blocked', models.ManyToManyField(related_name='blocked_by', blank=True, help_text='Profiles of users this user blocked.', to='findeco.UserProfile')),
                ('followees', models.ManyToManyField(related_name='followers', blank=True, help_text='Profiles of users this user follows.', to='findeco.UserProfile')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
