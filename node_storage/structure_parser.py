#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>,
# Klaus Greff <klaus.greff@gmx.net>
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
import re, unicodedata
from models import Node, Text
from factory import create_structureNode, create_slot

h1_start = re.compile(r"^\s*=(?P<title>[^=]+)=*\s*$", flags=re.MULTILINE)
general_h = re.compile(r"^\s*(={2,6}(?P<title>[^=]+)=*)\s*$", flags=re.MULTILINE)
invalid_symbols = re.compile(r"[^\w\-_\s]+")

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

REPLACEMENTS = {
          ord('ä'): 'ae',
          ord('ö'): 'oe',
          ord('ü'): 'ue',
          ord('ß'): 'ss',
          ord('Ä'): 'Ae',
          ord('Ö'): 'Oe',
          ord('Ü'): 'Ue',
          ord('ẞ'): 'SS',
        }

def substitute_umlauts(s):
    return s.translate(REPLACEMENTS)

def remove_unallowed_chars(s):
    s = invalid_symbols.sub('',s)
    return s

def remove_and_compress_whitespaces(s):
    return '_'.join(s.split())

def turn_into_valid_short_title(title, short_title_set=(), max_length=20):
    st = substitute_umlauts(title)
    st = strip_accents(st)
    st = remove_unallowed_chars(st)
    st = remove_and_compress_whitespaces(st)
    st = st[:min(len(st), max_length)]
    if not st:
        i = 0
        while True:
            i += 1
            new_st = str(i)
            if new_st not in short_title_set:
                return new_st
    if st not in short_title_set :
        return st
    else:
        i = 0
        while True:
            i += 1
            suffix = str(i)
            new_st = st[:min(max_length-len(suffix), len(st))] + suffix
            if new_st not in short_title_set:
                return new_st




def getHeadingMatcher(level=0):
    if 0 < level < 7:
        s = "%d"%level
    elif level == 0:
        s = "1, 6"
    else:
        raise ValueError("level must be between 1 and 6 or 0, but was %d."%level)
    return re.compile(r"^\s*={%s}(?P<title>[^=§]+)(?:§\s*(?P<short_title>[^=§\s]+)\s*)?=*\s*$"%s, flags=re.MULTILINE)



def validate_structure_schema(structure):
    """
    structure_node_schema = {
        'short_title':"string",
        'title':"string",
        'text':"wikiText",
        'children':[structure_node_schema,None]
    }
    """
    entries = [('short_title', unicode),
               ('title', unicode),
               ('text', unicode),
               ('children', list)]
    for n, t in entries:
        assert n in structure, "Required field '%s' is missing."%n
        assert type(structure[n]) is t, "Type of field '%s' should be %s but was %s"%(n, t, type(structure[n]))
    # validate short title
    assert 1 <= len(structure['short_title']) <= 20, "Length of short title must be between 1 and 20 (but was %d)."%len(structure['short_title'])
    # validate children
    for c in structure['children']:
        validate_structure_schema(c)
    return True

class InvalidWikiStructure(Exception):
    pass

def parse(s, short_title):
    #make sure we start with a heading 1
    m = h1_start.match(s)
    if m :
        title = m.groups("title")[0]
        title = title.partition("§")[0] # silently remove attempt to set short_title in H1
        s = h1_start.sub("", s)
    else :
        raise InvalidWikiStructure('Must start with H1 heading to set title')

    node = {
        'title':title.strip(),
        'short_title':short_title,
        'children':[]
    }

    # do we need a StructureNode or will a TextNode do?
    if not general_h.search(s) :
        # TextNode
        node['text'] = s.strip()
        return node
    # else : StructureNode

    # determine used header depth:
    level = 0
    for i in range(2, 7):
        m = getHeadingMatcher(i)
        if m.search(s):
            level = i
            break
    assert 1 < level < 7

    split_doc = m.split(s)
    # now the text before, between and after headings is split_doc[0::3]
    # the text of the headings are split_doc[1::3]
    # and the short titles (or None if omitted) are split_doc[2::3]

    # leading text is used to set text of structure node
    node['text'] = split_doc[0].strip()
    # assert that no headings are in that text
    if general_h.search(node['text']):
        raise InvalidWikiStructure("Cannot have headers in Node text")

    # iterate the headings, short_titles, and corresponding texts:
    short_title_set = set()
    for title, short_title, text in zip(split_doc[1::3], split_doc[2::3], split_doc[3::3]):
        # check if short_title is valid/unique/exists
        if not short_title or len(short_title.strip()) == 0:
            short_title=title
        short_title=turn_into_valid_short_title(short_title, short_title_set)
        short_title_set.add(short_title)

        node['children'].append(parse("= %s =\n"%title.strip() + text.strip(), short_title))

    return node

def create_structure_from_structure_node_schema(schema, parent_slot, authors, origin_group=[], argument=None):
    origin_found = False
    if len(origin_group) > 0 and argument:
        for origin in origin_group:
            if origin.title == schema['title'] and origin.text.text == schema['text'] and\
               [child['short_title'] for child in schema['children']] == [child.title for child in
                                                                          origin.children.all()]:
                structure = origin
                origin_found = True
        if not origin_found:
            structure = create_structureNode(long_title=schema['title'], text=schema['text'], authors=authors)
            parent_slot.append_child(structure)
            for origin in origin_group:
                origin.add_derivate(argument, structure)
    else:
        structure = create_structureNode(long_title=schema['title'], text=schema['text'], authors=authors)
        parent_slot.append_child(structure)
    for i, child in enumerate(schema['children']):
        if origin_found:
            child_slot = structure.children.all()[i]
        else:
            child_slot = create_slot(child['short_title'])
            structure.append_child(child_slot)
        sub_origin_group = []
        for origin in origin_group:
            for origin_slot in origin.children.filter(
                title__in=[child['short_title'] for child in schema['children']]).all():
                sub_origin_group += origin_slot.children.all()
        create_structure_from_structure_node_schema(child, child_slot, authors, sub_origin_group, argument)