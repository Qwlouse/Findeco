# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Activation.key'
        db.alter_column('findeco_activation', 'key', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'PasswordRecovery.key'
        db.alter_column('findeco_passwordrecovery', 'key', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Adding field 'UserProfile.api_key'
        db.add_column('findeco_userprofile', 'api_key',
                      self.gf('django.db.models.fields.CharField')(default=u'BDY8FSKP8C9C580C', max_length=16),
                      keep_default=False)


        # Changing field 'EmailActivation.key'
        db.alter_column('findeco_emailactivation', 'key', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Activation.key'
        db.alter_column('findeco_activation', 'key', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'PasswordRecovery.key'
        db.alter_column('findeco_passwordrecovery', 'key', self.gf('django.db.models.fields.CharField')(max_length=64))
        # Deleting field 'UserProfile.api_key'
        db.delete_column('findeco_userprofile', 'api_key')


        # Changing field 'EmailActivation.key'
        db.alter_column('findeco_emailactivation', 'key', self.gf('django.db.models.fields.CharField')(max_length=64))

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
        'findeco.activation': {
            'Meta': {'object_name': 'Activation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'XKKLCYPZD517913B6X36D54PYXSWVDWVKM4FB3HRDR6D0GSC3WFZ6F8118WZGZLZ'", 'max_length': '100'}),
            'key_valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'findeco.emailactivation': {
            'Meta': {'object_name': 'EmailActivation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'SV544KKPWXXZPKZF5BXSY7N1HW05P4R9BHBMWFFFK84TKTZGV9VB2XN5QBFXTRXX'", 'max_length': '100'}),
            'new_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'findeco.passwordrecovery': {
            'Meta': {'object_name': 'PasswordRecovery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'TQYYMG7M4HKB5ZPLNHV00YGSBBKLH31SM0C6M1BPM6G6RRSFH5DF84FRDG9BXQB9'", 'max_length': '100'}),
            'key_valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'findeco.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "u'4L8FQKT8B8TTQGYB'", 'max_length': '16'}),
            'blocked': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'blocked_by'", 'blank': 'True', 'to': "orm['findeco.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'followees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'followers'", 'blank': 'True', 'to': "orm['findeco.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified_until': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'verification_key': ('django.db.models.fields.CharField', [], {'default': "u'WD9K2973ZPX8NBLD8K0T8XSYR9X9TBC2V8SN0MBZCZ217CYZP3L1NPR1W0HG6CP8'", 'max_length': '64'})
        }
    }

    complete_apps = ['findeco']