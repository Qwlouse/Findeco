#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import re
import unicodedata

h1_start = re.compile(r"^\s*=(?P<title>[^=]+)=*[ \t]*")
valid_title = re.compile(r"[^=]+")
general_heading = re.compile(r"^\s*(={2,6}(?P<title>" + valid_title.pattern +
                             ")=*)\s*$", flags=re.MULTILINE)
invalid_symbols = re.compile(r"[^\w\-_\s]+")


def strip_accents(s):
    return ''.join(
        (c for c in unicodedata.normalize('NFD', s) if unicodedata.category(
            c) != 'Mn'))


REPLACEMENTS = {
    ord('ä'): 'ae',
    ord('ö'): 'oe',
    ord('ü'): 'ue',
    ord('ß'): 'ss',
    ord('Ä'): 'Ae',
    ord('Ö'): 'Oe',
    ord('Ü'): 'Ue',
    ord('ẞ'): 'SS'
}


def substitute_umlauts(s):
    return s.translate(REPLACEMENTS)


def remove_unallowed_chars(s):
    s = invalid_symbols.sub('', s)
    return s


def remove_and_compress_whitespaces(s):
    return '_'.join(s.split()).strip('_')


def turn_into_valid_short_title(title, short_title_set=(), max_length=20):
    st = substitute_umlauts(title)
    st = strip_accents(st)
    st = remove_unallowed_chars(st)
    st = remove_and_compress_whitespaces(st)
    st = st.lstrip('1234567890-_')
    st = st[:min(len(st), max_length)]
    if not st:
        st = 'sub'
    if st not in short_title_set:
        return st
    else:
        i = 0
        while True:
            i += 1
            suffix = str(i)
            new_st = st[:min(max_length - len(suffix), len(st))] + suffix
            if new_st not in short_title_set:
                return new_st


def get_heading_matcher(level=0):
    if 0 < level < 7:
        s = "%d" % level
    elif level == 0:
        s = "1, 6"
    else:
        raise ValueError(
            "level must be between 1 and 6 or 0, but was %d." % level)
    pattern = r"^\s*={%s}(?P<title>[^=§]+)" \
              r"(?:§\s*(?P<short_title>[^=§\s][^=§]*))?=*\s*$"
    return re.compile(pattern % s, flags=re.MULTILINE)