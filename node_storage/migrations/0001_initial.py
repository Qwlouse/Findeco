# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Derivation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='IndexCache',
            fields=[
                ('path', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('index_nodes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('node_type', models.CharField(choices=[('a', 'Argument'), ('l', 'StructureNode'), ('s', 'Slot')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='NodeOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PathCache',
            fields=[
                ('path', models.CharField(max_length=250, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SpamFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('authors', models.ManyToManyField(related_name='author_in', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextCache',
            fields=[
                ('path', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('paragraphs', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='node_storage.Node', primary_key=True, serialize=False)),
                ('arg_type', models.CharField(choices=[('p', 'pro'), ('c', 'con'), ('n', 'neut')], max_length=1)),
                ('index', models.IntegerField()),
            ],
            bases=('node_storage.node',),
        ),
        migrations.AddField(
            model_name='vote',
            name='nodes',
            field=models.ManyToManyField(related_name='votes', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='node',
            field=models.OneToOneField(related_name='text', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='spamflag',
            name='node',
            field=models.ForeignKey(related_name='spam_flags', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='spamflag',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pathcache',
            name='node',
            field=models.ForeignKey(related_name='paths', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='nodeorder',
            name='child',
            field=models.ForeignKey(related_name='parent_order_set', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='nodeorder',
            name='parent',
            field=models.ForeignKey(related_name='child_order_set', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='favorite',
            field=models.ForeignKey(to='node_storage.Node', blank=True, related_name='favorite_of', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='node',
            name='parents',
            field=models.ManyToManyField(through='node_storage.NodeOrder', related_name='children', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='sources',
            field=models.ManyToManyField(through='node_storage.Derivation', blank=True, related_name='derivates', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='derivation',
            name='derivate',
            field=models.ForeignKey(related_name='source_order_set', to='node_storage.Node'),
        ),
        migrations.AddField(
            model_name='derivation',
            name='source',
            field=models.ForeignKey(related_name='derivative_order_set', to='node_storage.Node'),
        ),
        migrations.AlterUniqueTogether(
            name='nodeorder',
            unique_together=set([('parent', 'child')]),
        ),
        migrations.AddField(
            model_name='derivation',
            name='argument',
            field=models.ForeignKey(blank=True, null=True, to='node_storage.Argument'),
        ),
        migrations.AddField(
            model_name='argument',
            name='concerns',
            field=models.ForeignKey(related_name='arguments', to='node_storage.Node'),
        ),
        migrations.AlterUniqueTogether(
            name='derivation',
            unique_together=set([('source', 'derivate')]),
        ),
    ]
