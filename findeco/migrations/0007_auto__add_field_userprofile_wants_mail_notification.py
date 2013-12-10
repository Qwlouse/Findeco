# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.wants_mail_notification'
        db.add_column(u'findeco_userprofile', 'wants_mail_notification',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'UserProfile.wants_mail_notification'
        db.delete_column(u'findeco_userprofile', 'wants_mail_notification')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'findeco.activation': {
            'Meta': {'object_name': 'Activation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'446ZVV4ND1QN0DX2T5NRHH04R16L60021L1W8WP3HYY4G08NQKN227WHW3F2Z41W'", 'max_length': '100'}),
            'key_valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'findeco.emailactivation': {
            'Meta': {'object_name': 'EmailActivation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'HHN50LCXQ1F8PB96WPC7YCPVZG8MQ51C3DBRM11L78RTPPZF9TXPPCS2LHBMH002'", 'max_length': '100'}),
            'new_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'findeco.passwordrecovery': {
            'Meta': {'object_name': 'PasswordRecovery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'7K46CKFN5L988BRTBF9292H97PKQ757T6DS0PX9YBXYWMSCKT837R8Z6QV8N5XGQ'", 'max_length': '100'}),
            'key_valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'findeco.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "u'Y5WC631BN5V448XF'", 'max_length': '16'}),
            'blocked': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'blocked_by'", 'blank': 'True', 'to': u"orm['findeco.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'followees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'followers'", 'blank': 'True', 'to': u"orm['findeco.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified_until': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'verification_key': ('django.db.models.fields.CharField', [], {'default': "u'69LCY0N972QSHHTWMX518882ZH5KZ3XZ7YG324LTV6B4K69TCLQ0KPP3RNTKSB1Q'", 'max_length': '64'}),
            'wants_mail_notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['findeco']