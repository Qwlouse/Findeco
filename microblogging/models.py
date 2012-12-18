#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>,
# Klaus Greff <klaus.greff@gmx.net>
# This file is part of CoDebAr.
#
# CoDebAr is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# CoDebAr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# CoDebAr. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import re
import node_storage as backend
from django.contrib.auth.models import User

user_ref_pattern = re.compile(r"(?:(?<=\s)|\A)@(?P<username>\w+)\b")
tag_pattern = re.compile(r"(?:(?<=\s)|\A)#(?P<tagname>\w+)\b")
internal_link_pattern = re.compile(r"(?:(?<=\s)|\A)(?P<path>/(?:[a-zA-Z0-9-_]+\.\d+/)*[a-zA-Z0-9-_]+(?:\.\d+)?/?)\b")
url_pattern = re.compile(r"(?:(?<=\s)|\A)((?:https?://)?[\da-z\.-]+\.[a-z\.]{2,6}[-A-Za-z0-9+&@#/%?=~_|!:,.;]*)\b")

def create_post(text, author):
    split_text = user_ref_pattern.split(text)
    mentions = []
    for i in range(1, len(split_text), 2):
        username = split_text[i]
        try:
            u = User.objects.get(username=username)
            split_text[i] = '<a href="/.users/{0}">@{0}</a>'.format(username)
            mentions.append(u)
        except User.DoesNotExist:
            split_text[i] = '@'+username
    text = "".join(split_text)

    split_text = tag_pattern.split(text)
    for i in range(1, len(split_text), 2):
        tagname = split_text[i]
        split_text[i] = '<a href="/.search?search_string=%23{0}">#{0}</a>'.format(tagname)
    text = "".join(split_text)

    split_text = internal_link_pattern.split(text)
    nodes = []
    for i in range(1, len(split_text), 2):
        path = split_text[i]
        try:
            n = backend.get_node_with_text_for_path(path)
            split_text[i] = '<a href="{0}">{1}</a>'.format(path, path.rsplit('/',1)[1])
            nodes.append(n)
        except ObjectDoesNotExist:
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


class Post(models.Model):
    node_references = models.ManyToManyField(
        backend.Node,
        symmetrical=False,
        related_name='microbloging_references',
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

    def __unicode__(self):
        return u'%s says "%s" on %s' % (self.author.username, self.text, self.time)


class Reference(models.Model):
    entry = models.ForeignKey(
        Post,
        related_name='references')
    time = models.DateTimeField('date referenced', auto_now=True)
    referencer = models.ForeignKey(
        User,
        related_name='microblogging_references')

    def __unicode__(self):
        return u'%s references "%s" on %s' % (self.referencer.username, self.entry, self.time)


def getFeedForUser(user):
    references = Reference.objects.filter(referencer=user).order_by('-time')
    referenced_entries = set()
    references_and_entries = []
    for reference in references:
        if not reference.entry_id in referenced_entries:
            referenced_entries.add(reference.entry_id)
            references_and_entries.append((reference, reference.entry))
    followed = Q(user__followers=user)
    own = Q(user = user)
    entries = Post.objects.filter(followed | own).order_by('-time')
    return [e for e in entries if not e.id in referenced_entries], references_and_entries