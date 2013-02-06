/* Findeco is dually licensed under GPLv3 or later and MPLv2.
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
##############################################################################*/

function ClassParser() {}

var Parser = new ClassParser();

var h1Start = "^\s*=(?P<title>[^=]+)=*\s*$";
var generalH = "^\s*(={2,6}(?P<title>[^=]+)=*)\s*$";
var invalidSymbols = "[^\w\-_\s]+";

function getHeadingMatcher(level) {
    var s;
    if ((level < 7) && (level > 0)) {
        s = String(level);
    } else {
        if (level == 0) {
            s = "1, 6";
        } else {
            return false;
            /* raise ValueError("level must be between 1 and 6 or 0, but was %d."%level) */
        }
    }
    return "^\s*={" + s + "}(?P<title>[^=§]+)(?:§\s*(?P<short_title>[^=§\s][^=§]*))?=*\s*$"
}

function removeUnallowedChars(s) {
    return s.replace(invalidSymbols, '');
}

function removeAndCompressWhitespaces(s) {
    var words = s.split(" ")
    var compressed = ""
    for (var i = 0; i < words.length; i++) {
        compressed += "_" + words[i];
    }
    return compressed.substring(1)
}

function substituteUmlauts(s) {
    var umlauts = ['ä','ö','ü','ß','Ä','Ö','Ü','ẞ'];
    var substuitutes = ['ae','oe','ue','ss','Ae','Oe','Ue','SS'];
    for (var i = 0; i < umlauts.length; i++) {
        s = s.replace(umlauts[i],substuitutes[i]);
    }
    return s;
}

function turnIntoValidShortTitle(title, shortTitleSet, maxLength) {
    var st = substituteUmlauts(title);
    st = strip_accents(st);
    st = removeUnallowedChars(st);
    st = removeAndCompressWhitespaces(st);
    st = st.substring(0, maxLength);
    if (st.length <= 0) {
        var i = 0;
        while (true) {
            i += 1;
            var new_st = String(i)
            var not_found = true;
            for (var j = 0; j < shortTitleSet.length; j++) {
                if (new_st == shortTitleSet[j]) {
                    not_found = false;
                }
            }
            if (not_found) {
                return new_st;
            }
        }
    }
    not_found = true;
    for (j = 0; j < shortTitleSet.length; j++) {
        if (st == shortTitleSet[j]) {
            not_found = false;
        }
    }
    if (not_found) {
        return st;
    } else {
        i = 0;
        while (true) {
            i++;
            var suffix = String(i);
            new_st = st.substring(0, maxLength - suffix.length) + suffix;
            not_found = true;
            for (j = 0; j < shortTitleSet.length; j++) {
                if (new_st == shortTitleSet[j]) {
                    not_found = false;
                }
            }
            if (not_found) {
                return new_st
            }
        }
    }
}

function parseStructure(s, shortTitle) {
    var m = s.match(h1Start);
    if(m.length > 1){
        var title = m[1];
        title = title.split("§")[0]; /* silently remove attempt to set short_title in H1 */
        s = s.replace(h1Start,"");
    } else {
        return false;
        /*raise InvalidWikiStructure('Must start with H1 heading to set title')*/
    }
    title = title.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    title = title.substring(0, 150);
    var node = [];
    node['title'] = title.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    node['short_title'] = shortTitle;
    node['children'] = [];

    /* do we need a StructureNode or will a TextNode do? */
    if (!(s.match(generalH).length <= 1)) {
        /* Text Node */
        node['text'] = s.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
        return node
    } /* else: StructureNode */

    /* determine used header depth: */
    var level = 0;
    for(var i= 2; i<7; i++) {
        m = getHeadingMatcher(i);
        if (s.match(m).length > 1) {
            level = i;
            break;
        }
    }

    var splitDoc = s.split(m);
    /* now the text before, between and after headings is splitDoc[0::3]
     the text of the headings are splitDoc[1::3]
     and the short titles (or None if omitted) are splitDoc[2::3] */

    /* leading text is used to set text of structure node */
    node['text'] = splitDoc[0].replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    /* assert that no headings are in that text */
    if(node['text'].match(generalH).length > 1) {
        return false;
        /* raise InvalidWikiStructure("Cannot have headers in Node text") */
    }

    /* iterate the headings, short_titles, and corresponding texts: */
    var shortTitleSet = [];
    var text = "";
    for (i = 1; i < (splitDoc.length-1)/3; i++) {
        title = splitDoc[1+i*3];
        shortTitle = splitDoc[2+i*3];
        text = splitDoc[3+i*3];
        /* check if short_title is valid/unique/exists */
        if ((shortTitle.length <= 0) || (shortTitle.replace(/^\s+|\s+$/g, '').length <= 0)) {
            shortTitle = title;}
        shortTitle = turnIntoValidShortTitle(shortTitle, shortTitleSet, 20);
        shortTitleSet.push(shortTitle);

        node['children'].push(parseStructure("= "+title.replace(/^\s+|\s+$/g, '')+" =\n" + text.replace(/^\s+|\s+$/g, ''), shortTitle))
    }
    return node;
}

ClassParser.prototype.parse = function(text){
    return "<p>Not Implemented!</p>";
};

