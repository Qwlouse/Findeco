# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        if orm['findeco.UserProfile'].objects.filter(user__username='Beschlossenes Programm').count() > 0:
            beschlossenes_programm_profile = orm['findeco.UserProfile'].objects.filter(
                user__username='Beschlossenes Programm').all()[0]
            beschlossenes_programm_profile.user.username = 'Beschluss_Programm'
            beschlossenes_programm_profile.user.save()
            if not beschlossenes_programm_profile.description:
                beschlossenes_programm_profile.description = "Diese Vorschläge wurden in ihrer urspünglichen " + \
                                                             "Fassung schon von einem Parteitag beschlossen. " + \
                                                             "Weiterentwicklungen dieser Vorschläge sind " + \
                                                             "natürlich kein beschlossenes Programm."
                beschlossenes_programm_profile.save()

    def backwards(self, orm):
        if orm['findeco.UserProfile'].objects.filter(user__username='Beschluss_Programm').count() > 0:
            beschlossenes_programm_profile = orm['findeco.UserProfile'].objects.filter(
                user__username='Beschluss_Programm').all()[0]
            beschlossenes_programm_profile.user.username = 'Beschlossenes Programm'
            beschlossenes_programm_profile.user.save()

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
            'key': ('django.db.models.fields.CharField', [], {'default': "u'8CW4X96H4WBGMQTV9QDL1V2HDPC9H9L5XXGQHDL60G7C239TSGB3QMV9SVWQYVRH'", 'max_length': '100'}),
            'key_valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'findeco.emailactivation': {
            'Meta': {'object_name': 'EmailActivation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'RFWSP29T0P31FFFH0GWM1HP8M1745BD0MD4ZLM7XWQW4FHVLR6FL2K0XPDS4D4WT'", 'max_length': '100'}),
            'new_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'findeco.passwordrecovery': {
            'Meta': {'object_name': 'PasswordRecovery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "u'C7L20CRR6L59GZSHMX4B5X9FVMCDWMRHKN40R7DY3WPRXQXK2CSVYWC8S0RWS6F6'", 'max_length': '100'}),
            'key_valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'findeco.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'api_key': ('django.db.models.fields.CharField', [], {'default': "u'YCDRYSKY06XNN134'", 'max_length': '16'}),
            'blocked': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'blocked_by'", 'blank': 'True', 'to': u"orm['findeco.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'followees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'followers'", 'blank': 'True', 'to': u"orm['findeco.UserProfile']"}),
            'help_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified_until': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'verification_key': ('django.db.models.fields.CharField', [], {'default': "u'NLMP76KGLPNBWPKDN11NF2KH599L6BNZ338Q612B7K1VZSM0F308CZGZV0PDF29S'", 'max_length': '64'}),
            'wants_mail_notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['findeco']
    symmetrical = True
