#!/usr/bin/python
# coding=utf-8
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
################################################################################

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import create_post
from ..views import load_microblogging
import node_storage as backend

class SimpleTest(TestCase):
    def test_post_creation(self):
        node1 = backend.models.Node()
        node1.save()
        text1 = backend.models.Text()
        text1.node = node1
        text1.text = "Testtext"
        max = User()
        max.username = "max"
        text1.author = max
        text2 = backend.models.Text()
        node2 = backend.models.Node()
        node2.save()
        text2.node = node2
        text2.text = "Testtext Nummer 2"
        text2.author = max
        max.save()
        text1.save()
        text2.save()
        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla gut.",max))
        posts.append(create_post("Ich finde /Blubb schlecht.", max))
        request = False
        request.user = max
        response = load_microblogging(request,"/Bla.1",0,"older")
        print(response)
        self.assertEqual(response,"{Zeuch}")

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
