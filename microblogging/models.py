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

from django.db import models
import re
from findeco.api_validation import USERNAME
import node_storage as backend
from django.contrib.auth.models import User
from django.utils.html import escape

WORDSTART = r"(?:(?<=\s)|\A)"
WORDEND = r"\b"


def keyword(pattern):
    return re.compile(WORDSTART + pattern + WORDEND)

user_ref_pattern = keyword("@" + USERNAME)
tag_pattern = keyword("#(?P<tagname>\w+)")
internal_link_pattern = keyword(r"(?P<path>/(?:[a-zA-Z0-9-_]+\.\d+/)*[a-zA-Z0-9-_]+(?:\.\d+)?/?)")

url_pattern = keyword(r"((?:https?://)?[\da-z\.-]+\.[a-z\.]{2,6}[-A-Za-z0-9+&@#/%?=~_|!:,.;]*)")


class Post(models.Model):
    node_references = models.ManyToManyField(
        backend.Node,
        symmetrical=False,
        related_name='microblogging_references',
        blank=True)
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='microblogging_posts')
    mentions = models.ManyToManyField(
        User,
        related_name='mentioning_entries',
        symmetrical=False,
        blank=True)
    time = models.DateTimeField('date posted', auto_now=True)
    is_reference_to = models.ForeignKey(
        'self',
        related_name='referenced',
        blank=True,
        null=True)

    def __unicode__(self):
        if self.is_reference_to:
            return u'%s references "%s" by %s on %s' % (
                self.author.username,
                self.text,
                self.is_reference_to.author.username,
                self.time)
        else:
            return u'%s says "%s" on %s' % (self.author.username,
                                            self.text,
                                            self.time)


def create_post(text, author, path=None, do_escape=True):
    if do_escape:
        text = escape(text)
    split_text = user_ref_pattern.split(text)
    mentions = []
    for i in range(1, len(split_text), 2):
        username = split_text[i]
        try:
            u = User.objects.get(username=username)
            split_text[i] = '<a href="/#/user/{0}">@{0}</a>'.format(username)
            mentions.append(u)
        except User.DoesNotExist:
            split_text[i] = '@' + username
    text = "".join(split_text)

    split_text = tag_pattern.split(text)
    for i in range(1, len(split_text), 2):
        tagname = split_text[i]
        split_text[i] = '<a href="/#/search/{0}">#{0}</a>'.format(tagname)
    text = "".join(split_text)

    split_text = internal_link_pattern.split(text)
    nodes = []
    if path is not None:
        nodes.append(backend.get_node_for_path(path))
    for i in range(1, len(split_text), 2):
        path = split_text[i]
        try:
            n = backend.get_node_for_path(path)
            if n.node_type == backend.Node.SLOT:
                slot = n
                n = backend.get_favorite_if_slot(n)
                position = backend.NodeOrder.objects.filter(child=n).filter(
                    parent=slot).all()[0].position
                path += "." + str(position)
            split_text[i] = '<a href="{0}">{1}</a>'.format(
                '/#' + path, path.rsplit('/', 1)[1])
            nodes.append(n)
        except backend.IllegalPath:
            pass
    text = "".join(split_text)

    split_text = url_pattern.split(text)
    for i in range(1, len(split_text), 2):
        link = split_text[i]
        split_text[i] = '<a href="{0}">{0}</a>'.format(link)
    text = "".join(split_text)

    post = Post()
    post.text = text
    post.author = author
    post.save()
    post.mentions.add(*mentions)
    post.node_references.add(*nodes)
    post.save()
    return post