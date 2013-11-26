#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
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
from django.core import mail
from django.db.models import Q
from django.test import TestCase
from microblogging.api_validation import validate_response
from findeco.error_handling import ViewError
from microblogging.factory import create_post
from microblogging.view_helpers import (
    microblogging_response, get_load_type, convert_long_urls,
    send_notification_to)
from node_storage.factory import create_user


class ViewHelpersTest(TestCase):
    ################## get_load_type_query #####################################

    def test_get_load_type_query_without_options(self):
        t, i = get_load_type({})
        self.assertEqual(t, "newer")
        self.assertEqual(i, -1)

    def test_get_load_type_query_with_load_type_only_raises(self):
        with self.assertRaises(ViewError):
            get_load_type({'type': 'newer'})

        with self.assertRaises(ViewError):
            get_load_type({'type': 'older'})

        with self.assertRaises(ViewError):
            get_load_type({'type': 'foobar', 'id': 2})

    def test_get_load_type_query_with_options(self):
        t, i = get_load_type({'type': 'newer', 'id': 2})
        self.assertEqual(t, "newer")
        self.assertEqual(i, 2)

        t, i = get_load_type({'type': 'older', 'id': 5})
        self.assertEqual(t, "older")
        self.assertEqual(i, 5)

    ################## microblogging_response ##################################

    def test_microblogging_response_empty(self):
        response = microblogging_response(Q(), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(validate_response(response.content,
                                          "load_microblogging"))

    def test_microblogging_response_limited_to_20_newest_sorted(self):
        hugo = create_user("hugo")
        for i in range(25):
            create_post("text%d" % i, hugo)
        response = microblogging_response(Q(), {})
        self.assertTrue(validate_response(response.content,
                                          "load_microblogging"))
        result = json.loads(response.content)["loadMicrobloggingResponse"]
        self.assertEqual(len(result), 20)
        self.assertEqual([p['microblogID'] for p in result], range(25, 5, -1))

    def test_microblogging_response_limited_to_newer_sorted(self):
        hugo = create_user("hugo")
        for i in range(25):
            create_post("text%d" % i, hugo)
        response = microblogging_response(Q(), {"type": "newer", "id": 3})
        self.assertTrue(validate_response(response.content,
                                          "load_microblogging"))
        result = json.loads(response.content)["loadMicrobloggingResponse"]
        self.assertEqual(len(result), 20)
        self.assertEqual([p['microblogID'] for p in result], range(23, 3, -1))

    def test_microblogging_response_limited_to_older_sorted(self):
        hugo = create_user("hugo")
        for i in range(25):
            create_post("text%d" % i, hugo)
        response = microblogging_response(Q(), {"type": "older", "id": 24})
        self.assertTrue(validate_response(response.content,
                                          "load_microblogging"))
        result = json.loads(response.content)["loadMicrobloggingResponse"]
        self.assertEqual(len(result), 20)
        self.assertEqual([p['microblogID'] for p in result], range(23, 3, -1))

    ################## convert_long_urls #######################################

    def test_convert_long_urls_removes_hostname_from_structure_node_path(self):
        text = convert_long_urls("text http://www.hostname.de/foo.1/ text",
                                 "www.hostname.de")
        self.assertEqual(text, "text /foo.1/ text")

        text = convert_long_urls("text https://www.hostname.de/foo.1 text",
                                 "www.hostname.de")
        self.assertEqual(text, "text /foo.1 text")

    def test_convert_long_urls_removes_hostname_from_argument_path(self):
        text = convert_long_urls(
            "text http://www.hostname.de/foo.1/ba.2.con.7 text",
            "www.hostname.de")
        self.assertEqual(text, "text /foo.1/ba.2.con.7 text")

        text = convert_long_urls(
            "text http://www.hostname.de/foo.1/ba.2.con.7/ text",
            "www.hostname.de")
        self.assertEqual(text, "text /foo.1/ba.2.con.7/ text")

    def test_convert_long_urls_leaves_hostname_for_non_node_path(self):
        text = convert_long_urls("text http://www.hostname.de/imprint text",
                                 "www.hostname.de")
        self.assertEqual(text, "text http://www.hostname.de/imprint text")

    def test_convert_long_urls_converts_user_urls(self):
        text = convert_long_urls("text http://www.hostname.de/user/admin text",
                                 "www.hostname.de")
        self.assertEqual(text, "text @admin text")

    def test_convert_long_urls_leaves_hostname_for_root_path(self):
        text = convert_long_urls("text http://www.hostname.de text",
                                 "www.hostname.de")
        self.assertEqual(text, "text http://www.hostname.de text")

        text = convert_long_urls("text http://www.hostname.de/ text",
                                 "www.hostname.de")
        self.assertEqual(text, "text http://www.hostname.de/ text")

    ################## send_notification_to ####################################

    def test_send_notification_to_sends_mail_via_bcc(self):
        hugo = create_user("hugo")
        post = create_post('my test posttext', hugo)
        send_notification_to(post, ['foo@bar.de', 'bar@foo.de'])
        self.assertEqual(len(mail.outbox), 1)
        m = mail.outbox[0]
        self.assertEqual(m.to, [])
        self.assertEqual(m.bcc, ['foo@bar.de', 'bar@foo.de'])
        self.assertIn('my test posttext', m.body)
        self.assertIn('hugo', m.subject)
