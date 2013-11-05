#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>,
# Klaus Greff <klaus.greff@gmx.net>
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
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
from __future__ import division, print_function, unicode_literals
import re
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext

import node_storage as backend

WORDSTART = r"(?:(?<=\s)|\A)"
WORDEND = r"\b"


NODE_LINK_TEMPLATE = '<a href="/{}">{}<span class="nodeIndex">{}</span></a>'

def keyword(pattern):
    return re.compile(WORDSTART + pattern + WORDEND)

tag_pattern = keyword(r"#(?P<tagname>\w+)")
url_pattern = keyword(r"((?:https?://)?[\da-z\.-]+\.[a-z\.]{2,6}"
                      r"[-A-Za-z0-9+&@#/%?=~_|!:,.;]*)")


class Post(models.Model):
    USER_POST = 'p'
    NODE_CREATED = 'c'
    NODE_REFINED = 'r'
    SPAM_MARKED = 's'
    SPAM_UNMARKED = 'n'
    NODE_FOLLOWED = 'f'
    NODE_UNFOLLOWED = 'u'
    ARGUMENT_CREATED = 'a'
    MICROBLOGGING_TYPE = (
        (USER_POST, 'userpost'),
        (NODE_CREATED, 'node_created'),
        (NODE_REFINED, 'node_refined'),
        (SPAM_MARKED, 'node_spam_marked'),
        (SPAM_UNMARKED, 'node_spam_unmarked'),
        (NODE_FOLLOWED, 'node_followed'),
        (NODE_UNFOLLOWED, 'node_unfollowed'),
        (ARGUMENT_CREATED, 'argument_created')
    )

    node_references = models.ManyToManyField(
        backend.Node,
        symmetrical=False,
        related_name='microblogging_references',
        blank=True)
    location = models.ForeignKey(
        backend.Node,
        related_name='microblogging_from_here',
        blank=False,
        null=False)
    text_cache = models.TextField()
    text_template = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='microblogging_posts')
    mentions = models.ManyToManyField(
        User,
        related_name='mentioning_entries',
        symmetrical=False,
        blank=True)
    time = models.DateTimeField('date posted', auto_now_add=True)
    post_type = models.CharField(max_length=1, choices=MICROBLOGGING_TYPE)
    is_answer_to = models.ForeignKey(
        'self',
        related_name='referenced',
        blank=True,
        null=True)

    @classmethod
    def short_post_type(cls, arg_type):
        return {None: cls.USER_POST,
                'userpost': cls.USER_POST,
                'node_created': cls.NODE_CREATED,
                'node_refined': cls.NODE_REFINED,
                'node_spam_marked': cls.SPAM_MARKED,
                'node_spam_unmarked': cls.SPAM_UNMARKED,
                'node_followed': cls.NODE_FOLLOWED,
                'node_unfollowed': cls.NODE_UNFOLLOWED,
                cls.USER_POST: cls.USER_POST,
                cls.NODE_CREATED: cls.NODE_CREATED,
                cls.NODE_REFINED: cls.NODE_REFINED,
                cls.SPAM_MARKED: cls.SPAM_MARKED,
                cls.SPAM_UNMARKED: cls.SPAM_UNMARKED,
                cls.NODE_FOLLOWED: cls.NODE_FOLLOWED,
                cls.NODE_UNFOLLOWED: cls.NODE_UNFOLLOWED
                }[arg_type]

    def render(self):
        user_dict = {
            'u' + str(i): '<a href="/user/{0}">@{0}</a>'.format(u.username)
            for i, u in enumerate(self.mentions.order_by('id'))
        }
        node_dict = {
            'n' + str(i): create_html_for_node(n)
            for i, n in enumerate(self.node_references.order_by('id'))
        }
        format_dict = dict()
        format_dict.update(user_dict)
        format_dict.update(node_dict)

        # get template
        if self.post_type == self.USER_POST:
            template = preprocess_userpost_template(self.text_template)
        else:
            template = SYSTEM_MESSAGE_TEMPLATES[self.post_type]

        # insert references and mentions
        try:
            text = template.format(**format_dict)
        except KeyError:
            import warnings
            warnings.warn('corrupted text_template')
            text = 'CORRUPTED: ' + template

        self.text_cache = text
        self.save()

    def __unicode__(self):
        if self.is_answer_to:
            return u'%s references "%s" by %s on %s' % (
                self.author.username,
                self.text_cache,
                self.is_answer_to.author.username,
                self.time)
        else:
            return u'%s says "%s" on %s' % (self.author.username,
                                            self.text_cache,
                                            self.time)


def create_html_for_node(node):
    path = node.get_a_path()
    title = node.title
    split_path = path.rsplit('.', 1)
    index = split_path[1] if len(split_path) > 1 else 1
    return NODE_LINK_TEMPLATE.format(path, title, index)


def preprocess_userpost_template(template):
    # escape html
    processed_template = escape(template)
    # replace #hashtags by links to search
    split_text = tag_pattern.split(processed_template)
    for i in range(1, len(split_text), 2):
        tagname = split_text[i]
        split_text[i] = '<a href="/search/{0}">#{0}</a>'.format(tagname)
    processed_template = "".join(split_text)
    # replace external links
    split_text = url_pattern.split(processed_template)
    for i in range(1, len(split_text), 2):
        link = split_text[i]
        split_text[i] = '<a href="{0}">{0}</a>'.format(link)
    processed_template = "".join(split_text)
    return processed_template


SYSTEM_MESSAGE_TEMPLATES = {
    Post.NODE_CREATED: ugettext('node_created_message'),
    Post.NODE_REFINED: ugettext('node_refined_message'),
    Post.SPAM_MARKED: ugettext('node_flagged_as_spam_message'),
    Post.SPAM_UNMARKED: ugettext('node_unflagged_as_spam_message'),
    Post.NODE_FOLLOWED: ugettext('node_followed_message'),
    Post.NODE_UNFOLLOWED: ugettext('node_unfollowed_message'),
    Post.ARGUMENT_CREATED: ugettext('argument_created_message'),
}