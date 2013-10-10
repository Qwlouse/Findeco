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
"""
Pathparser 

Paths are of the form:
  PATH = (NODE + '/')* + [SUFFIX] + ['/']
  SHORT_TITLE = ALPHA + (ALPHANUM | '_' | '-'){0:19}
  ID = POSITIVE_INT
  SUFFIX = ARGUMENT_SUFFIX | SLOT_SUFFIX | NODE_SUFFIX
  SLOT_SUFFIX = SHORT_TITLE
  NODE_SUFFIX = SLOT_SUFFIX + '.' + ID
  ARGUMENT_SUFFIX = NODE_SUFFIX + '.' + ('pro' | 'neut' | 'con') + ['.' + ID]

Examples:

  Bildung
  Bildung.7/
  Bildung.7/Hochschule.8/Akkreditierung.1
  Foo_bar.1/L33.7
  Datenschutz.1/Einleitung
  Transparenz.2.pro
  Transparenz.2.con.12
"""
from __future__ import division, print_function, unicode_literals
import re

SHORT_TITLE = r'(?:[a-zA-Z][a-zA-Z0-9-_]{0,19})'
ID = r'(?:[0-9]+)'
SLOT = SHORT_TITLE
NODE = '(?:' + SLOT + r'\.' + ID + ')'
ARG_CATEGORY = r'(?:' + NODE + r'\.' + '(?:pro|neut|con|all)' + ')'
ARG = r'(?:' + NODE + r'\.' + '(?:pro|neut|con|all)' + r'(?:\.' + ID + '))'
SUFFIX = r'(?:' + ARG + '|' + ARG_CATEGORY + '|' + NODE + '|' + SLOT + ')'
RESTRICTED_SUFFIX = r'(?:' + ARG + '|' + NODE + ')'
PATH = '(?P<path>' + '(?:' + NODE + '/' + ')*' + SUFFIX + '?' + ')' + '/?'
RESTRICTED_PATH = '(?P<path>' + '(?:' + NODE + '/' + ')*' + RESTRICTED_SUFFIX +\
                  '?' + ')' + '/?'
RESTRICTED_NONROOT_PATH = '(?P<path>' + '(?:' + NODE + '/' + ')+' + \
                          RESTRICTED_SUFFIX + '?' + ')' + '/?'
pathMatcher = re.compile(PATH)


def parse_suffix(path):
    path = path.strip('/')
    if not path:
        return "", {}
    parts = path.rsplit('/', 1)
    prefix, suffix = parts if len(parts) == 2 else ("", path)
    parts = suffix.split('.')
    if len(parts) == 1:
        return prefix, {'slot': suffix}
    prefix = (prefix + '/' + parts[0] + '.' + parts[1]).strip('/')
    path_type = {}
    if len(parts) >= 3:
        path_type['arg_type'] = parts[2]
    if len(parts) == 4:
        path_type['arg_id'] = int(parts[3])

    return prefix, path_type


def parse_path(path):
    path = path.strip('/')  # strip leading and trailing slashes
    parts = path.split('/')
    nodes = []
    for p in parts[:-1]:
        short_title, node_id = p.split('.')
        nodes.append((short_title, int(node_id)))
    last = parts[-1].split('.')
    if len(last) == 1:
        if last[0]:
            last = dict(slot=last[0])
        else:
            last = {}
    else:  # len(last) >= 2 because zero is impossible
        nodes.append((last[0], int(last[1])))
        last = dict(zip(['arg_type', 'arg_id'], last[2:]))
        if 'arg_id' in last:
            last['arg_id'] = int(last['arg_id'])
    return nodes, last
