# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.location'
        db.add_column('microblogging_post', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1,
                                                                            related_name=u'microblogging_from_here',
                                                                            to=orm['node_storage.Node']),
                      keep_default=False)

        # Adding field 'Post.text_cache'
        db.add_column('microblogging_post', 'text_cache',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Post.text_template'
        db.add_column('microblogging_post', 'text_template',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Post.post_type'
        db.add_column('microblogging_post', 'post_type',
                      self.gf('django.db.models.fields.CharField')(default='p', max_length=1),
                      keep_default=False)

        # Renaming field 'Post.is_reference_to' to 'Post.is_answer_to'
        db.rename_column('microblogging_post', 'is_reference_to_id', 'is_answer_to_id')

    def backwards(self, orm):
        # Renaming field 'Post.is_answer_to' to 'Post.is_reference_to'
        db.rename_column('microblogging_post', 'is_answer_to_id', 'is_reference_to_id')

        # Adding field 'Post.text'
        db.add_column('microblogging_post', 'text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Post.location'
        db.delete_column('microblogging_post', 'location_id')

        # Deleting field 'Post.text_template'
        db.delete_column('microblogging_post', 'text_template')

        # Deleting field 'Post.post_type'
        db.delete_column('microblogging_post', 'post_type')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')",
                     'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'microblogging.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [],
                       {'related_name': "u'microblogging_posts'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_answer_to': ('django.db.models.fields.related.ForeignKey', [],
                             {'blank': 'True', 'related_name': "u'referenced'", 'null': 'True',
                              'to': "orm['microblogging.Post']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "u'microblogging_from_here'", 'to': "orm['node_storage.Node']"}),
            'mentions': ('django.db.models.fields.related.ManyToManyField', [],
                         {'symmetrical': 'False', 'related_name': "u'mentioning_entries'", 'blank': 'True',
                          'to': "orm['auth.User']"}),
            'node_references': ('django.db.models.fields.related.ManyToManyField', [],
                                {'symmetrical': 'False', 'related_name': "u'microblogging_references'", 'blank': 'True',
                                 'to': "orm['node_storage.Node']"}),
            'post_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_cache': ('django.db.models.fields.TextField', [], {}),
            'text_template': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'node_storage.argument': {
            'Meta': {'object_name': 'Argument', '_ormbases': ['node_storage.Node']},
            'arg_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'concerns': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "u'arguments'", 'to': "orm['node_storage.Node']"}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [],
                         {'to': "orm['node_storage.Node']", 'unique': 'True', 'primary_key': 'True'})
        },
        'node_storage.derivation': {
            'Meta': {'unique_together': "((u'source', u'derivate'),)", 'object_name': 'Derivation'},
            'argument': ('django.db.models.fields.related.ForeignKey', [],
                         {'to': "orm['node_storage.Argument']", 'null': 'True', 'blank': 'True'}),
            'derivate': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "u'source_order_set'", 'to': "orm['node_storage.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [],
                       {'related_name': "u'derivative_order_set'", 'to': "orm['node_storage.Node']"})
        },
        'node_storage.node': {
            'Meta': {'object_name': 'Node'},
            'favorite': ('django.db.models.fields.related.ForeignKey', [],
                         {'blank': 'True', 'related_name': "u'favorite_of'", 'null': 'True',
                          'on_delete': 'models.SET_NULL', 'to': "orm['node_storage.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [],
                        {'related_name': "u'children'", 'symmetrical': 'False',
                         'through': "orm['node_storage.NodeOrder']", 'to': "orm['node_storage.Node']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [],
                        {'symmetrical': 'False', 'related_name': "u'derivates'", 'blank': 'True',
                         'through': "orm['node_storage.Derivation']", 'to': "orm['node_storage.Node']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'node_storage.nodeorder': {
            'Meta': {'unique_together': "((u'parent', u'child'),)", 'object_name': 'NodeOrder'},
            'child': ('django.db.models.fields.related.ForeignKey', [],
                      {'related_name': "u'parent_order_set'", 'to': "orm['node_storage.Node']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [],
                       {'related_name': "u'child_order_set'", 'to': "orm['node_storage.Node']"}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['microblogging']