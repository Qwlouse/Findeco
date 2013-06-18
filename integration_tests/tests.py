#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import division, print_function, unicode_literals
import unittest
from django.test import TestCase
from libs.selexe.selexe_runner import SelexeRunner
from findeco.project_path import project_path


# Example how to use selenium testrunner to run a testcase
class SelTest(TestCase):
    def setUp(self):

        pass

    def test_content_page_does_not_contain_root(self):
        selexe = SelexeRunner(project_path('integration_tests/testcases/ContentPageRoot'))
        res = selexe.run()
        self.assertListEqual(res, [])

    def test_user_lifecycle(self):
        selexe = SelexeRunner(project_path('integration_tests/testcases/UserRegistration'))
        res = selexe.run()
        self.assertListEqual(res, [])
        selexe = SelexeRunner(project_path('integration_tests/testcases/UserLogin'))
        res = selexe.run()
        self.assertListEqual(res, [])
        selexe = SelexeRunner(project_path('integration_tests/testcases/UserProfile'))
        res = selexe.run()
        self.assertListEqual(res, [])
        selexe = SelexeRunner(project_path('integration_tests/testcases/UserDelete'))
        res = selexe.run()
        self.assertListEqual(res, [])

if __name__ == '__main__':
    unittest.main()