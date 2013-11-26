#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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
#endregion #####################################################################
from __future__ import division, print_function, unicode_literals
import json
import re
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils.translation import ugettext
from findeco import settings
from findeco.api_validation import USERNAME
from findeco.error_handling import InvalidMicrobloggingOptions
from findeco.paths import RESTRICTED_NONROOT_PATH
from findeco.view_helpers import json_response

from .models import Post
from .tools import convert_to_response_list


def convert_long_urls(text, hostname):
    """
    This function removes the unnecessary part from urls which are copy&pasted
    from the url field of the browser.
    """
    hostname_path_pattern = re.compile(r"(https?://)?" +
                                       r"(" + re.escape(hostname) + r")/" +
                                       r"(?=" + RESTRICTED_NONROOT_PATH +
                                       r"(?:\s|$))")

    username_pattern = re.compile(r"(https?://)?" +
                                  r"(" + re.escape(hostname) + r")/user/" +
                                  r"(?=" + USERNAME + r"(?:\s|$))")

    text = hostname_path_pattern.sub("/", text)
    text = username_pattern.sub("@", text)

    return text


def get_load_type(options):
    if "type" in options or 'id' in options:
        if not ('type' in options and 'id' in options):
            raise InvalidMicrobloggingOptions(json.dumps(options))

        if options["type"] not in ["newer", "older"]:
            raise InvalidMicrobloggingOptions(json.dumps(options))

        return options["type"], int(options["id"])

    else:
        return "newer", -1


def get_posts(query, options):
    load_type, load_id = get_load_type(options)
    posts = Post.objects.filter(query).distinct()
    if load_id == -1:
        return posts.order_by('-id')[:20]
    else:
        if load_type == "newer":
            return reversed(posts.filter(id__gt=load_id).order_by('id')[:20])
        elif load_type == "older":
            return posts.filter(id__lt=load_id).order_by('-id')[:20]


def microblogging_response(query, options):
    posts = get_posts(query, options)
    return json_response({
        'loadMicrobloggingResponse': convert_to_response_list(posts)})


def get_microblogging_for_authored_nodes_query(named_user):
    return (Q(node_references__text__authors=named_user) |
            Q(location__text__authors=named_user))


def get_microblogging_from_user_query(named_user):
    return Q(author=named_user)


def get_mentions_query(named_user):
    return Q(mentions=named_user)


def get_timeline_query(named_user):
    return (Q(author=named_user) |
            Q(author__in=named_user.profile.followees.all()))


def get_microblogging_for_node_query(node):
    return Q(location=node) | Q(node_references=node)


def get_microblogging_for_followed_nodes_query(named_user):
    return (Q(node_references__votes__user=named_user) |
            Q(location__votes__user=named_user))


def send_derivate_notification(post, mailing_list):
    subject = ugettext('derivate_email_notification_subject')
    send_notification_to(subject, post, mailing_list)


def send_mention_notification(post, mailing_list):
    subject = ugettext('userpost_email_notification_subject{author}').format(
        author=post.author.username)
    send_notification_to(subject, post, mailing_list)


def send_notification_to(subject, post, mailing_list):
    body = convert_local_links_to_absolute(post.text_cache)
    email = EmailMessage(subject,
                         body,
                         settings.EMAIL_HOST_USER,
                         to=[], bcc=mailing_list)
    print('sending to ', mailing_list)
    email.send(fail_silently=True)


def notify_users(post):
    mentioned = post.mentions.filter(profile__wants_mail_notification=True)
    mailing_list = [user.email for user in mentioned]
    send_mention_notification(post, mailing_list)


def notify_derivate(node, post):
    follows_for_notifying = node.votes.filter(
        user__profile__wants_mail_notification=True).all()
    mailing_list = [vote.user.email for vote in follows_for_notifying]
    send_derivate_notification(post, mailing_list)


def convert_local_links_to_absolute(html):
    return html.replace(' href="/', ' href="' + settings.FINDECO_BASE_URL + '/')
