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

from django.contrib.auth.models import User

from node_storage.path_helpers import get_node_for_path


def parse_microblogging(text, author, location, time=None, references_to=None):
    """
    Parse the text of a Microblog-Post and turn it into a JSON Structure that
    can then easily be
    """
    pass


def validate_microblogging_schema(structure):
    """
    MICROBLOG_POST = {
        'author': user_id,
        'location': node_id,
        'time': timestamp,
        'text': text,
        'mentions': [user_id, None],  # have to be sorted and unique
        'references': [path, None],   # have to be sorted and unique
        'answer_to': microblog_id     # -1 if not an answer
    }
    """
    entries = [('author', int),
               ('location', int),
               ('time', int),
               ('text', unicode),
               ('mentions', list),
               ('references', list),
               ('answer_to', int)]
    for n, t in entries:
        assert n in structure, "Required field '%s' is missing." % n
        e = structure[n]
        assert isinstance(e,  t), \
            "Type of field '%s' should be %s but was %s" % (n, t, type(e))

    # validate mentions
    mentions = structure['mentions']
    assert mentions == sorted(mentions), "mentions must be sorted!"
    assert len(set(mentions)) == len(mentions), "mentions must be unique!"
    for m in mentions:
        assert isinstance(m,  int), \
            "mentions have to be IDs (int) but was of type %s" % type(m)
        User.objects.get(id=m)

    # validate node_references
    references = structure['references']
    assert references == sorted(references), "references must be sorted!"
    assert len(set(references)) == len(references), "references must be unique!"
    for r in references:
        assert isinstance(r,  unicode), \
            "references have to be paths (unicode) but was %s" % type(r)
        get_node_for_path(r)  # raises Illegal Path if invalid path


    return True