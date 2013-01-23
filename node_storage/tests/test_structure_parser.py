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
from django.test import TestCase
from ..structure_parser import strip_accents, substitute_umlauts
from ..structure_parser import remove_unallowed_chars, turn_into_valid_short_title

class StructureParserTest(TestCase):
    def test_strip_accents(self):
        self.assertEqual(strip_accents("aäàáâeèéêiìíîoöòóôuüùúû"),
                                       "aaaaaeeeeiiiiooooouuuuu")

    def test_substitute_umlauts(self):
        self.assertEqual(substitute_umlauts("Haßloch"), "Hassloch")
        self.assertEqual(substitute_umlauts("HAẞLOCH"), "HASSLOCH")
        self.assertEqual(substitute_umlauts("Köln"), "Koeln")
        self.assertEqual(substitute_umlauts("Ülm"), "Uelm")

    def test_remove_unallowed_chars(self):
        self.assertEqual(remove_unallowed_chars("abc()[]{}<>?!.,:;+^`~|$#%def"), "abcdef")

    def test_remove_unallowde_chars_keeps_allowed_chars(self):
        valid = "abcdefghijklmnopqrstuvwxyz-1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.assertEqual(remove_unallowed_chars(valid), valid)

    def test_turn_into_valid_short_title(self):
        titles = [
            ("schöner Titel was?", "schoener_Titel_was"),
            ("viiiiiieeeeeel zuuuuuuu laaaaaaaang", "viiiiiieeeeeel_zuuuu"),
            ("viel )()()(()()( zu {}{}{}{ lang", "viel_zu_lang"),
            ("","1"),
            ("N0body is as L€€+.a$.m3", "N0body_is_as_Lam3")
        ]
        for t, st in titles:
            self.assertEqual(turn_into_valid_short_title(t), st)


