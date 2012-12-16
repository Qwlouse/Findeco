#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
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
"""
Paths are of the form:
  PATH = '/' + (SHORT_TITLE + '.' + ID + '/')* + [SUFFIX] + ['/']
  SHORT_TITLE = ALPHA + (ALPHANUM | '_' | '-'){0:19}
  ID = POSITIVE_INT
  SUFFIX = SLOT_SUFFIX | ARGUMENT_SPEC
  SLOT_SUFFIX = '/' + SHORT_TITLE
  ARGUMENT_SUFFIX = '.' + ('pro' | 'neut' | 'con') + ['.' + ID]

Examples:
  /
  /Bildung
  /Bildung.7/
  /Bildung.7/Hochschule.8/Akkreditierung.1
  /Foo_bar.1/L33.7
  /Datenschutz.1/Einleitung
  /Transparenz.2.pro
  /Transparenz.2.con.12
"""
from __future__ import division, print_function, unicode_literals
import re

SHORT_TITLE = r'([a-zA-Z][a-zA-Z0-9-_]{0,19})'
ID = r'([0-9]+)'
SLOT_SUFFIX = '(/'+SHORT_TITLE+')'
ARG_SUFFIX = r'((\.pro' + '|' + r'\.neut' + '|' + r'\.con)' + r'(\.' + ID +')?)'
SUFFIX = r'(' + SLOT_SUFFIX + '|' + ARG_SUFFIX + ')'
PATH = r'(?P<path>(/' + SHORT_TITLE + r'\.' + ID + ')*' + SUFFIX + '?)/?'

pathMatcher = re.compile(PATH)
