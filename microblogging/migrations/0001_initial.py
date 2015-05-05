# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('node_storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('text_cache', models.TextField()),
                ('text_template', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='date posted')),
                ('post_type', models.CharField(choices=[('p', 'userpost'), ('c', 'node_created'), ('r', 'node_refined'), ('s', 'node_spam_marked'), ('n', 'node_spam_unmarked'), ('f', 'node_followed'), ('u', 'node_unfollowed'), ('a', 'argument_created')], max_length=1)),
                ('author', models.ForeignKey(related_name='microblogging_posts', to=settings.AUTH_USER_MODEL)),
                ('is_answer_to', models.ForeignKey(blank=True, related_name='referenced', null=True, to='microblogging.Post')),
                ('location', models.ForeignKey(related_name='microblogging_from_here', to='node_storage.Node')),
                ('mentions', models.ManyToManyField(blank=True, related_name='mentioning_entries', to=settings.AUTH_USER_MODEL)),
                ('node_references', models.ManyToManyField(blank=True, related_name='microblogging_references', to='node_storage.Node')),
            ],
        ),
    ]
