#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2014 Johannes Merkert <jonny@pinae.net>
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

from __future__ import division, print_function, unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
import json
from findeco.tests.helpers import assert_is_error_response

from node_storage import get_root_node
from node_storage.factory import create_slot, create_user, create_textNode
from node_storage.factory import create_structureNode, create_argument
from node_storage.factory import create_vote, create_spam_flag
from ..view_helpers import create_index_node_for_slot


class LoadArgumentNewsTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

        self.root = get_root_node()
        self.slot1 = create_slot('Wahlprogramm')
        self.root.append_child(self.slot1)
        self.structureNode1 = create_structureNode('LangerWahlprogrammTitel',
                                                   authors=[self.hans])
        self.slot1.append_child(self.structureNode1)
        self.slot11 = create_slot('Transparenz')
        self.structureNode1.append_child(self.slot11)
        self.textnode11 = create_textNode('Traaaansparenz', authors=[self.hans])
        self.slot11.append_child(self.textnode11)
        self.slot12 = create_slot('Bildung')
        self.structureNode1.append_child(self.slot12)
        self.textnode12 = create_textNode('Biiildung', authors=[self.hans])
        self.slot12.append_child(self.textnode12)
        self.slot13 = create_slot('Datenschutz')
        self.structureNode1.append_child(self.slot13)
        self.textnode13 = create_textNode('Daaatenschutz', authors=[self.hans])
        self.slot13.append_child(self.textnode13)

        for i in range(1, 25):
            arg = create_argument(self.textnode11, 'p', "Argument" + str(i),
                                  "Text of argument no. " + str(i), [self.hugo, self.hans])
            create_vote(self.hugo, [arg])
            if i % 2 == 1:
                create_vote(self.hans, [arg])
                create_spam_flag(self.hugo, [arg])

    def test_returns_last_arguments(self):
        response = self.client.get(reverse('load_argument_news'))
        parsed = json.loads(response.content)
        self.assertIn('loadArgumentNewsResponse', parsed)
        self.assertEqual(len(parsed['loadArgumentNewsResponse']), 20)
        for number, resultEntry in enumerate(parsed['loadArgumentNewsResponse']):
            self.assertEqual(resultEntry['node']['path'], u'Wahlprogramm.1/Transparenz.1')
            self.assertListEqual(resultEntry['node']['authorGroup'], [u'hans'])
            self.assertEqual(resultEntry['argument']['path'], u'Wahlprogramm.1/Transparenz.1.pro.' + str(24 - number))
            self.assertListEqual(resultEntry['argument']['authorGroup'], [u'hans', u'hugo'])
            if number % 2 == 0:
                self.assertEqual(resultEntry['argument']['followingCount'], 1)
                self.assertEqual(resultEntry['argument']['flaggingCount'], 0)
            else:
                self.assertEqual(resultEntry['argument']['followingCount'], 2)
                self.assertEqual(resultEntry['argument']['flaggingCount'], 1)