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



def parse(s, author, parent_slot):
    #make sure we start with a heading 1
    m = h1_start.match(s) # TODO: match short titles and warn about
    if m :
        title = m.groups("title")[0]
        title = title.partition("§")[0] # silently remove attempt to set short_title in H1
        s = h1_start.sub("", s)
    else :
        # TODO: warn about missing title
        title = parent_slot.short_title

    node = Node()
    node.parents.create(parent_slot)
    node.save()

    # do we need a StructureNode or will a TextNode do?
    if not general_h.search(s) :
        # TextNode
        t = Text()
        t.text = "= %s =\n"%title.strip() + s.strip()
        t.author = author
        t.node = node
        t.save()
        return t
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
    # what do we do now?

    # leading text is used to construct an "Einleitung" Slot and TextNode
    introduction = Node()
    introduction.parents.create(node)
    introduction.save()

    introduction_slot = Node()
    introduction_slot.parents.create(introduction)
    introduction_slot.save()
    introduction_slot_short_title = Text()
    introduction_slot_short_title.text = "Einleitung"
    introduction_slot_short_title.node = introduction_slot
    introduction_text_node = Node()
    introduction_text_node.parents.create(introduction_slot)
    introduction_text_node.save()
    introduction_text = Text()
    intro_text = split_doc[0]
    # assert that no headings are in intro-text
    if general_h.search(intro_text):
        # TODO: Warn!
        intro_text = general_h.sub(r"~\1", intro_text)
        #general_h.
    introduction_text.text = "= %s =\n"%title + intro_text

    introduction_text.node = introduction_text_node
    introduction_text.save()



    # iterate the headings, short_titles, and corresponding texts:
    short_title_set = set()
    for title, short_title, text in zip(split_doc[1::3], split_doc[2::3], split_doc[3::3]):
        # check if short_title is valid/unique/exists
        if not short_title or len(short_title.strip()) == 0:
            short_title=title[:min(15, len(title))]

        # make short titles valid
        short_title = short_title[:min(20, len(short_title))]
        short_title = strip_accents(short_title)
        short_title = invalid_symbols.sub('',short_title)
        if short_title in short_title_set:
            i = 1
            while short_title + str(i) in short_title_set:
                i += 1
            short_title += str(i)

        short_title_set.add(short_title)
        slot = Node()
        slot.parents.create(node)
        slot.save()
        slot_text = Text()
        slot_text.text = short_title.strip().replace(" ", "_")
        slot_text.node = slot
        slot_text.save()
        parse("= %s =\n"%title.strip() + text.strip(), slot)
    return node