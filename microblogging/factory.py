#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>
# This file is part of Findeco.
#
# Findeco is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# Findeco is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Findeco. If not, see <http://www.gnu.org/licenses/>.
###############################################################################
#
###############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

import re
from django.contrib.auth.models import User

from findeco.api_validation import USERNAME
from findeco.paths import RESTRICTED_PATH
from microblogging.models import Post
from node_storage.path_helpers import get_node_for_path, IllegalPath


def keyword(pattern):
    WORDSTART = r"(?:(?<=\s)|\A)"
    WORDEND = r"\b"
    return re.compile(WORDSTART + pattern + WORDEND)

MENTION_PATTERN = keyword("@" + USERNAME)
REFERENCE_PATTERN = keyword(r'/' + RESTRICTED_PATH)


def extract_references(text):
    references = set()
    for r in set(re.findall(REFERENCE_PATTERN, text)):
        try:
            get_node_for_path(r)
            references.add(r)
        except IllegalPath:
            pass
    references = sorted(references)

    def reference_sub(m):
        path = m.group().strip('/')
        if path in references:
            return "{n%d}" % references.index(path)
        else:
            return '/' + path

    template_text, _ = re.subn(REFERENCE_PATTERN, reference_sub, text)
    return references, template_text


def extract_mentions(text):
    mentions = dict()
    for m in set(re.findall(MENTION_PATTERN, text)):
        try:
            mentions[m.lower()] = User.objects.get(username__iexact=m).id
        except User.DoesNotExist:
            pass

    sorted_mentions = sorted(mentions.values())

    def mention_sub(m):
        username = m.group().strip('@').lower()
        if username in mentions:
            return "{u%d}" % sorted_mentions.index(mentions[username])
        else:
            return '@' + username

    template_text, _ = re.subn(MENTION_PATTERN, mention_sub, text)
    return sorted_mentions, template_text


def parse_microblogging(text, author, location, answer_to=None):
    """
    Parse the text of a Microblog-Post and turn it into a JSON Structure that
    can then easily be turned into a database entry
    """
    references, template_text = extract_references(text)
    mentions, template_text = extract_mentions(template_text)

    return {
        'author': author.id,
        'location': get_node_for_path(location).id,
        'type': "userpost",
        'template_text': template_text,
        'mentions': mentions,
        'references': [get_node_for_path(p) for p in references],
        'answer_to': answer_to
    }


def create_post_from_schema(schema):
    """
    Creates a Post-object out of a Post-schema and saved it to the database.
    The Object is returned.
    """
    post = Post.objects.create(
        author_id=schema['author'],
        post_type=Post.short_post_type(schema['type']),
        text_template=schema['template_text'],
        location_id=schema['location'],
        is_answer_to=schema['answer_to']
    )
    post.mentions = schema['mentions']
    post.node_references = schema['references']
    return post


def create_post(text, author, location='', answer_to=None):
    """
    Create a post from a given text.
    """
    schema = parse_microblogging(text, author, location, answer_to)
    post = create_post_from_schema(schema)
    post.render()
    return post


def validate_microblogging_schema(structure):
    """
    MICROBLOG_POST = {
        'author': user_id,
        'location': node_id,
        'type': one of [userpost, node_created, node_refined, node_spam_marked,
                        node_spam_unmarked, node_followed, node_unfollowed]
        'template_text': text,
        'mentions': [user_id, None],  # have to be sorted and unique
        'references': [path, None],   # have to be sorted and unique
        'answer_to': microblog_id     # -1 if not an answer
    }
    """
    entries = [('author', int),
               ('location', int),
               ('type', str),
               ('template_text', str),
               ('mentions', list),
               ('references', list),
               ('answer_to', int)]
    for n, t in entries:
        assert n in structure, "Required field '%s' is missing." % n
        e = structure[n]
        assert isinstance(e,  t), \
            "Type of field '%s' should be %s but was %s" % (n, t, type(e))

    # validate type
    allowed_types = {"userpost", "node_created", "node_refined",
                     "node_spam_marked", "node_spam_unmarked",
                     "node_followed", "node_unfollowed"}

    assert structure['type'] in allowed_types, \
        "Invalid type '%s'" % structure['type']

    # validate mentions
    mentions = structure['mentions']
    assert mentions == sorted(mentions), "mentions must be sorted!"
    assert len(set(mentions)) == len(mentions), "mentions must be unique!"
    for m in mentions:
        assert isinstance(m,  int), \
            "mentions have to be IDs (int) but was of type %s" % type(m)
        User.objects.get(id=m)

    # validate node_references
    references = structure['references']
    assert references == sorted(references), "references must be sorted!"
    assert len(set(references)) == len(references), "references must be unique"
    for r in references:
        assert isinstance(r,  str), \
            "references have to be paths (str) but was %s" % type(r)
        get_node_for_path(r)  # raises Illegal Path if invalid path

    return True
