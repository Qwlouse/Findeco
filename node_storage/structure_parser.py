#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# #############################################################################
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
# #############################################################################
#
# #############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

import re

from node_storage.path_helpers import get_good_path_for_structure_node
from node_storage.factory import create_structureNode, create_slot, create_vote
from node_storage.models import Node
from node_storage.validation import (h1_start, general_heading, get_heading_matcher,
                                     turn_into_valid_short_title)


def validate_structure_schema(structure):
    """
    structure_node_schema = {
        'short_title':"string",
        'title':"string",
        'text':"wikiText",
        'children':[structure_node_schema,None]
    }
    """
    entries = [('short_title', str),
               ('title', str),
               ('text', str),
               ('children', list)]
    for n, t in entries:
        assert n in structure, "Required field '%s' is missing." % n
        assert type(
            structure[n]) is t, "Type of field '%s' should be %s but was %s" % \
                                (n, t, type(structure[n]))
        # validate short title
    assert 1 <= len(structure['short_title']) <= 20, \
        "Length of short title must be between 1 and 20 (but was %d)." % len(
            structure['short_title'])
    # validate children
    for c in structure['children']:
        validate_structure_schema(c)
    return True


class InvalidWikiStructure(Exception):
    pass


def parse(s, short_title):
    # make sure we start with a heading 1
    m = h1_start.match(s)
    if m:
        title = m.groups("title")[0]
        # silently remove attempt to set short_title in H1
        title = title.partition("§")[0]
        s = h1_start.sub("", s)
    else:
        raise InvalidWikiStructure('Must start with H1 heading to set title')

    title = title.strip()
    title = title[:min(150, len(title))]
    node = {
        'title': title.strip(),
        'short_title': short_title,
        'children': []
    }

    # do we need a StructureNode or will a TextNode do?
    if not general_heading.search(s):
        # TextNode
        node['text'] = s.strip()
        return node
        # else : StructureNode

    # determine used header depth:
    level = 0
    for i in range(2, 7):
        m = get_heading_matcher(i)
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
    if general_heading.search(node['text']):
        raise InvalidWikiStructure("Cannot have headers in Node text")

    # iterate the headings, short_titles, and corresponding texts:
    short_title_set = set()
    for title, short_title, text in zip(split_doc[1::3], split_doc[2::3],
                                        split_doc[3::3]):
        # check if short_title is valid/unique/exists
        if not short_title or len(short_title.strip()) == 0:
            short_title = title
        short_title = turn_into_valid_short_title(short_title, short_title_set)
        short_title_set.add(short_title)

        node['children'].append(
            parse("= %s =\n" % title.strip() + text.strip(), short_title))

    return node


def split_title_from_text(text):
    m = h1_start.match(text)
    if m:
        title = m.groups("title")[0]
        # silently remove attempt to set short_title in H1
        title = title.partition("§")[0].strip()
        text = re.sub(h1_start, "", text).strip()
        return title, text
    else:
        raise InvalidWikiStructure('Must start with H1 heading to set title')


def get_title_from_text(text):
    # make sure we start with a heading 1
    m = h1_start.match(text)
    if m:
        title = m.groups("title")[0]
        # silently remove attempt to set short_title in H1
        title = title.partition("§")[0]
        return title.strip()
    else:
        raise InvalidWikiStructure('Must start with H1 heading to set title')


def create_structure_from_structure_node_schema(schema, parent_slot, author,
                                                clone_candidates=None):
    if not clone_candidates:
        clone_candidates = []
    clone_found = False
    for candidate in clone_candidates:
        if candidate.title == schema['title'] and \
           candidate.text.text == schema['text'] and \
           [child['short_title'] for child in schema['children']] == \
                [child.title for child in candidate.children.all()]:
            structure = candidate
            clone_found = True
    if not clone_found:
        structure = create_structureNode(long_title=schema['title'],
                                         text=schema['text'], authors=[author])
        parent_slot.append_child(structure)

        # auto-follows
        create_vote(author, [structure])

    for child in schema['children']:
        if clone_found:
            child_slot = structure.children.get(title=child['short_title'])
        else:
            child_slot = create_slot(child['short_title'])
            structure.append_child(child_slot)
        sub_clone_candidate_group = []
        for candidate in clone_candidates:
            for candidate_slot in candidate.children.filter(
                    title=child['short_title']).all():
                sub_clone_candidate_group += candidate_slot.children.all()
        create_structure_from_structure_node_schema(child, child_slot, author,
                                                    sub_clone_candidate_group)
    return structure


def create_derivate_from_structure_node_schema(schema, parent_slot, author,
                                               origin, score_tree,
                                               arg_type=None,
                                               arg_title="", arg_text=""):
    new_path_couples = []
    clone_found = False
    if origin.title == schema['title'] and \
       origin.text.text == schema['text'] and \
       [child['short_title'] for child in schema['children']] == \
            [child.title for child in origin.children.all()]:
        structure = origin
        clone_found = True
    if not clone_found:
        structure = create_structureNode(long_title=schema['title'],
                                         text=schema['text'], authors=[author])
        # auto-follow node
        create_vote(author, [structure])
        # append node
        parent_slot.append_child(structure)
        arg = origin.add_derivate(structure, arg_type=arg_type,
                                  title=arg_title, text=arg_text,
                                  authors=[author])

        # auto-follow argument
        #create_vote(author, [arg])
        # data for microblogging message
        new_path_couples.append(
            (get_good_path_for_structure_node(origin, parent_slot),
             get_good_path_for_structure_node(structure, parent_slot)))

    for child in schema['children']:
        if clone_found:
            child_slot = structure.children.get(title=child['short_title'])
        else:
            if child['short_title'] in score_tree['slots']:
                child_slot = origin.children.get(title=child['short_title'])
            else:
                child_slot = create_slot(child['short_title'])
            structure.append_child(child_slot)

        best = 0, None  # score, id
        if child['short_title'] in score_tree['slots']:
            for candidate in score_tree['slots'][child['short_title']]:
                if candidate['score'] >= best[0]:
                    best = candidate['score'], candidate

        if best[0] > 0:
            sub_origin = Node.objects.get(id=best[1]['id'])
            _, sub_path_couples = create_derivate_from_structure_node_schema(
                child, child_slot, author, sub_origin, best[1], arg_type,
                arg_title, arg_text)
            new_path_couples += sub_path_couples
        else:
            create_structure_from_structure_node_schema(child, child_slot,
                                                        author, [])

    return structure, new_path_couples
