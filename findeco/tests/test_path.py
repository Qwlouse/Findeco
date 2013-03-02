#!/usr/bin/python
# coding=utf-8
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
################################################################################
from __future__ import division, print_function, unicode_literals

from django.test import TestCase

from ..paths import pathMatcher, parse_path, parse_suffix


class PathRegExTest(TestCase):
    def test_matches_valid_paths(self):
        valid_paths = [
            "",
            "Bildung",
            "Bildung/",
            "Bildung.2",
            "Bildung.8/",
            "Bildung.6/Einleitung",
            "Bildung.7/Einleitung.4",
            "Bildung.1/Einleitung.3/foo.7",
            "Bildung.1/Einleitung.3/foo.7/first.1/second.2/third.3/fourth",
            "JustTwentyCharacters",
            "JustTwentyCharacters.20",
            "JustTwentyCharacters.20/JustTwentyCharacters.20/",
            "Hy-phens.3/Under_scores.4/Numb3rs.1",
            "A1234.4321/B123",
            "longID.1234567890/is_ok",
            "path.4/with.2/argument.2.pro",
            "path.4/with.2/argument.2.con",
            "path.4/with.2/argument.2.neut",
            "path.4/with.2/argument.2.pro.2",
            "path.4/with.2/argument.2.neut.4",
            "path.4/with.2/argument.2.con.7"
        ]
        for vp in valid_paths:
            m = pathMatcher.match(vp)
            self.assertIsNotNone(m)
            self.assertEqual(m.group(), vp)

    def test_does_not_match_invalid_paths(self):
        invalid_paths = [
            "/"
            "/StartingSlash",
            "/StartingSlash.12/but_rest_ok.1",
            "two.dots.12/foo",
            "missing.3.slash.3"
            "worng.1D/foo",
            "1stCharIsNumber.2/foo.12",
            "MoreThanTwentyCharacters.4/foo.12",
            "foo.2/MoreThanTwentyCharacters",
            "umläut.4/foo",
            "unallow$d.1/foo.2",
            "unallow#d.2/foo.2",
            "unallow|d.3/foo.2",
            "unallow:d.4/foo.2",
            "unallow?d.5/foo.2",
            "path.4/with.2/argument.2.pro/inbetween",
            "path.4/with.2/argument.2.neut/inbetween",
            "path.4/with.2/argument.2.con/inbetween",
            "path.4/with.2/argument.2.pro.2/inbetween",
            "path.4/with.2/argument.2.neut.7/inbetween",
            "path.4/with.2/argument.2.con.6/inbetween"]
        for ip in invalid_paths:
            m = pathMatcher.match(ip)
            if m:
                self.assertNotEqual(m.group(), ip)

    def test_parse_suffix(self):
        desired = [
            ("", "", {}),
            ("Bildung", "", {'slot':'Bildung'}),
            ("Bildung/", "", {'slot':'Bildung'}),
            ("Bildung.2", "Bildung.2", {}),
            ("Bildung.8/", "Bildung.8", {}),
            ("Bildung.6/Einleitung", "Bildung.6", {'slot':'Einleitung'}),
            ("Bildung.7/Einleitung.4", "Bildung.7/Einleitung.4", {}),
            ("Bildung.1/Einleitung.3/foo.7",
             "Bildung.1/Einleitung.3/foo.7",
             {}),
            ("path.4/with.2/argument.2.pro",
             "path.4/with.2/argument.2",
             {'arg_type':'pro'}),
            ("path.4/with.2/argument.2.neut",
             "path.4/with.2/argument.2",
             {'arg_type':'neut'}),
            ("path.4/with.2/argument.2.con",
             "path.4/with.2/argument.2",
             {'arg_type':'con'}),
            ("path.4/foo.2.con.7",
             "path.4/foo.2",
             {'arg_type':'con', 'arg_id':7})
        ]
        for path, nodes, last in desired:
            n, l = parse_suffix(path)
            self.assertEqual(nodes, n)
            self.assertEqual(last, l)

    def test_path_parsing(self):
        desired = [
            ("", [], {}),
            ("Bildung", [], {'slot':'Bildung'}),
            ("Bildung/", [], {'slot':'Bildung'}),
            ("Bildung.2", [('Bildung', 2)], {}),
            ("Bildung.8/", [('Bildung', 8)], {}),
            ("Bildung.6/Einleitung", [('Bildung', 6)], {'slot':'Einleitung'}),
            ("Bildung.7/Einleitung.4", [('Bildung', 7), ('Einleitung', 4)], {}),
            ("Bildung.1/Einleitung.3/foo.7",
                [('Bildung', 1), ('Einleitung', 3), ('foo', 7)],
                {}),
            ("path.4/with.2/argument.2.pro",
                [('path', 4), ('with', 2), ('argument', 2)],
                {'arg_type':'pro'}),
            ("path.4/with.2/argument.2.neut",
                [('path', 4), ('with', 2), ('argument', 2)],
                {'arg_type':'neut'}),
            ("path.4/with.2/argument.2.con",
                [('path', 4), ('with', 2), ('argument', 2)],
                {'arg_type':'con'}),
            ("path.4/foo.2.con.7",
                [('path', 4), ('foo', 2)],
                {'arg_type':'con', 'arg_id':7})
        ]
        for path, nodes, last in desired:
            n, l = parse_path(path)
            self.assertEqual(nodes, n)
            self.assertEqual(last, l)