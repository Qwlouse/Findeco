# -*- coding: utf-8 -*-
import datetime
import re
import collections
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.utils.html import strip_tags, escape
from findeco.paths import RESTRICTED_PATH
from node_storage.models import PathCache, Node, Argument
from node_storage.path_helpers import get_root_node
from microblogging.factory import parse_microblogging

WORDSTART = r"(?:(?<=\s)|\A)"
WORDEND = r"\b"


def keyword(pattern):
    return re.compile(WORDSTART + pattern + WORDEND)

tag_pattern = keyword(r"#(?P<tagname>\w+)")
url_pattern = keyword(r"((?:https?://)?[\da-z\.-]+\.[a-z\.]{2,6}"
                      r"[-A-Za-z0-9+&@#/%?=~_|!:,.;]*)")


def warn_then_missing_string():
    import warnings
    warnings.warn('corrupted text_template')
    return "MISSING"


class Migration(DataMigration):
    def replace_node_references(self, text):
        parts = re.compile(r'<a href="/(?:#/)?' + RESTRICTED_PATH + '">.*?</a>').split(text)
        for i in range(1, len(parts), 2):
            parts[i] = '/' + parts[i]
        return ''.join(parts)

    def node_get_a_path(self, n):
        """
        Returns a path which needn't be the only valid path to the node.
        """
        paths = PathCache.objects.filter(node=n)
        if paths.count() > 0:
            return paths[0].path
        else:
            # Note: This should NEVER happen
            # but since it did we have a backup plan here
            # TODO Remove if we are absolutely sure that every node is in PathCache

            if n.parents.count() == 0:
                return ""
            if n.node_type == Node.ARGUMENT:
                self_as_arg = Argument.objects.filter(argument_id=n.id).all()[0]
                npath = self_as_arg.concerns.get_a_path().strip('/')
                return '%s.%s.%d' % (npath, self_as_arg.arg_type, self_as_arg.index)
            parent = n.parents.all()[0]
            if self.node_type == Node.SLOT:
                suffix = n.title
            else:
                suffix = "." + str(self.get_index(parent)) + "/"
            path = parent.get_a_path() + suffix
            # write to path
            PathCache.objects.create(node=n, path=path)
            return path

    def post_render(self, post):
        user_dict = {
            'u' + str(i): u'<a href="/user/{0}">@{0}</a>'.format(u.username)
            for i, u in enumerate(post.mentions.order_by('id'))
        }
        node_dict = {
            'n' + str(i): u'<a href="/{}">{}</a>'.format(self.node_get_a_path(n), n.title)
            for i, n in enumerate(post.node_references.order_by('id'))
        }
        print(node_dict)
        format_dict = collections.defaultdict(warn_then_missing_string)
        format_dict.update(user_dict)
        format_dict.update(node_dict)
        # escape html
        text = escape(post.text_template)
        # insert references and mentions
        text = text.format(**format_dict)
        # replace #hashtags by links to search
        split_text = tag_pattern.split(text)
        for i in range(1, len(split_text), 2):
            tagname = split_text[i]
            split_text[i] = u'<a href="/search/{0}">#{0}</a>'.format(tagname)
        text = "".join(split_text)
        # replace external links
        split_text = url_pattern.split(text)
        for i in range(1, len(split_text), 2):
            link = split_text[i]
            split_text[i] = u'<a href="{0}">{0}</a>'.format(link)
        text = "".join(split_text)

        post.text_cache = text
        post.save()

    def get_location_and_references(self, candidates, references):
        """
        Findes the one reference which is not mentioned in the text. If all are mentioned in the text it returns the
        first one.
        :rtype : (node, [node])
        """
        try:
            location_id = candidates[0].id
        except IndexError:
            if len(references) > 0:
                location_id = references[0].id
            else:
                location_id = get_root_node().id
        new_references = []
        for candidate in candidates:
            if not candidate.id in [x.id for x in references]:
                location_id = candidate.id
            else:
                new_references.append(candidate)
        return location_id, new_references

    def forwards(self, orm):
        for post in orm['microblogging.Post'].objects.all():
            text = self.replace_node_references(post.text)
            text = strip_tags(text)

            schema = parse_microblogging(text, post.author, '/', get_root_node())
            post.text_template = schema['template_text']
            post.location.id, post.node_references =\
                self.get_location_and_references(list(post.node_references.all()), schema['references'])
            if post.node_references.count() < len(schema['references']):
                print("Missing reference! Adding location to node references.")
                post.node_references.add(post.location)
            if post.node_references.count() < len(schema['references']):
                print("Missing reference! Using references from the Text.")
                post.node_references = [orm['node_storage.Node'].objects.get(id=r.id) for r in schema['references']]
            self.post_render(post)
            post.save()

    def backwards(self, orm):
        for post in orm['microblogging.Post'].objects.all():
            post.text = post.text_cache
            post.save()

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
        'microblogging.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'microblogging_posts'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_answer_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'referenced'", 'null': 'True', 'to': "orm['microblogging.Post']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'microblogging_from_here'", 'to': "orm['node_storage.Node']"}),
            'mentions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'mentioning_entries'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'node_references': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'microblogging_references'", 'blank': 'True', 'to': "orm['node_storage.Node']"}),
            'post_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_cache': ('django.db.models.fields.TextField', [], {}),
            'text_template': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
        'node_storage.node': {
            'Meta': {'object_name': 'Node'},
            'favorite': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'favorite_of'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['node_storage.Node']"}),
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
        }
    }

    complete_apps = ['microblogging']
    symmetrical = True
