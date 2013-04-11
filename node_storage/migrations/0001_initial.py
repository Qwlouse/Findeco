# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('node_storage_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('favorite', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'favorite_of', null=True, to=orm['node_storage.Node'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('node_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('node_storage', ['Node'])

        # Adding model 'Argument'
        db.create_table('node_storage_argument', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['node_storage.Node'], unique=True, primary_key=True)),
            ('arg_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('concerns', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'arguments', to=orm['node_storage.Node'])),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('node_storage', ['Argument'])

        # Adding model 'Text'
        db.create_table('node_storage_text', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.OneToOneField')(related_name=u'text', unique=True, to=orm['node_storage.Node'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('node_storage', ['Text'])

        # Adding M2M table for field authors on 'Text'
        db.create_table('node_storage_text_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('text', models.ForeignKey(orm['node_storage.text'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('node_storage_text_authors', ['text_id', 'user_id'])

        # Adding model 'Derivation'
        db.create_table('node_storage_derivation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('derivate', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'source_order_set', to=orm['node_storage.Node'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'derivative_order_set', to=orm['node_storage.Node'])),
            ('argument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['node_storage.Argument'], null=True, blank=True)),
        ))
        db.send_create_signal('node_storage', ['Derivation'])

        # Adding unique constraint on 'Derivation', fields ['source', 'derivate']
        db.create_unique('node_storage_derivation', ['source_id', 'derivate_id'])

        # Adding model 'NodeOrder'
        db.create_table('node_storage_nodeorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('child', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'parent_order_set', to=orm['node_storage.Node'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'child_order_set', to=orm['node_storage.Node'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('node_storage', ['NodeOrder'])

        # Adding unique constraint on 'NodeOrder', fields ['parent', 'child']
        db.create_unique('node_storage_nodeorder', ['parent_id', 'child_id'])

        # Adding model 'Vote'
        db.create_table('node_storage_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('node_storage', ['Vote'])

        # Adding M2M table for field nodes on 'Vote'
        db.create_table('node_storage_vote_nodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vote', models.ForeignKey(orm['node_storage.vote'], null=False)),
            ('node', models.ForeignKey(orm['node_storage.node'], null=False))
        ))
        db.create_unique('node_storage_vote_nodes', ['vote_id', 'node_id'])

        # Adding model 'SpamFlag'
        db.create_table('node_storage_spamflag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'spam_flags', to=orm['node_storage.Node'])),
        ))
        db.send_create_signal('node_storage', ['SpamFlag'])

        # Adding model 'TextCache'
        db.create_table('node_storage_textcache', (
            ('path', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True)),
            ('paragraphs', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('node_storage', ['TextCache'])

        # Adding model 'IndexCache'
        db.create_table('node_storage_indexcache', (
            ('path', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True)),
            ('index_nodes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('node_storage', ['IndexCache'])

        # Adding model 'PathCache'
        db.create_table('node_storage_pathcache', (
            ('path', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'paths', to=orm['node_storage.Node'])),
        ))
        db.send_create_signal('node_storage', ['PathCache'])


    def backwards(self, orm):
        # Removing unique constraint on 'NodeOrder', fields ['parent', 'child']
        db.delete_unique('node_storage_nodeorder', ['parent_id', 'child_id'])

        # Removing unique constraint on 'Derivation', fields ['source', 'derivate']
        db.delete_unique('node_storage_derivation', ['source_id', 'derivate_id'])

        # Deleting model 'Node'
        db.delete_table('node_storage_node')

        # Deleting model 'Argument'
        db.delete_table('node_storage_argument')

        # Deleting model 'Text'
        db.delete_table('node_storage_text')

        # Removing M2M table for field authors on 'Text'
        db.delete_table('node_storage_text_authors')

        # Deleting model 'Derivation'
        db.delete_table('node_storage_derivation')

        # Deleting model 'NodeOrder'
        db.delete_table('node_storage_nodeorder')

        # Deleting model 'Vote'
        db.delete_table('node_storage_vote')

        # Removing M2M table for field nodes on 'Vote'
        db.delete_table('node_storage_vote_nodes')

        # Deleting model 'SpamFlag'
        db.delete_table('node_storage_spamflag')

        # Deleting model 'TextCache'
        db.delete_table('node_storage_textcache')

        # Deleting model 'IndexCache'
        db.delete_table('node_storage_indexcache')

        # Deleting model 'PathCache'
        db.delete_table('node_storage_pathcache')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'node_storage.argument': {
            'Meta': {'object_name': 'Argument', '_ormbases': ['node_storage.Node']},
            'arg_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'concerns': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'arguments'", 'to': "orm['node_storage.Node']"}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['node_storage.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'node_storage.derivation': {
            'Meta': {'unique_together': "((u'source', u'derivate'),)", 'object_name': 'Derivation'},
            'argument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['node_storage.Argument']", 'null': 'True', 'blank': 'True'}),
            'derivate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'source_order_set'", 'to': "orm['node_storage.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'derivative_order_set'", 'to': "orm['node_storage.Node']"})
        },
        'node_storage.indexcache': {
            'Meta': {'object_name': 'IndexCache'},
            'index_nodes': ('django.db.models.fields.TextField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'})
        },
        'node_storage.node': {
            'Meta': {'object_name': 'Node'},
            'favorite': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'favorite_of'", 'null': 'True', 'to': "orm['node_storage.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'children'", 'symmetrical': 'False', 'through': "orm['node_storage.NodeOrder']", 'to': "orm['node_storage.Node']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'derivates'", 'blank': 'True', 'through': "orm['node_storage.Derivation']", 'to': "orm['node_storage.Node']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'node_storage.nodeorder': {
            'Meta': {'unique_together': "((u'parent', u'child'),)", 'object_name': 'NodeOrder'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'parent_order_set'", 'to': "orm['node_storage.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'child_order_set'", 'to': "orm['node_storage.Node']"}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        'node_storage.pathcache': {
            'Meta': {'object_name': 'PathCache'},
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'paths'", 'to': "orm['node_storage.Node']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'})
        },
        'node_storage.spamflag': {
            'Meta': {'object_name': 'SpamFlag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'spam_flags'", 'to': "orm['node_storage.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'node_storage.text': {
            'Meta': {'object_name': 'Text'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'author_in'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'text'", 'unique': 'True', 'to': "orm['node_storage.Node']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'node_storage.textcache': {
            'Meta': {'object_name': 'TextCache'},
            'paragraphs': ('django.db.models.fields.TextField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'})
        },
        'node_storage.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'votes'", 'symmetrical': 'False', 'to': "orm['node_storage.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['node_storage']