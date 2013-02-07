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

var h1Start = /^\s*=([^=]+)=*\s*(.*)$/;
var generalH = /\s*={2,6}([^=]+)=*\s*/g;
var invalidSymbols = /[^\w\-_\s]+/g;

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
    return "(?:[^=]|^)={"+s+"}([^=§]+)(?:§([^=]+)=|()=)=*(?:([^=].*)|()$)";
}

function removeUnallowedChars(s) {
    return s.replace(invalidSymbols, '');
}

function removeAndCompressWhitespaces(s) {
    var words = s.split(" ");
    var compressed = "";
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
    //st = strip_accents(st);
    st = removeUnallowedChars(st);
    st = removeAndCompressWhitespaces(st);
    st = st.substring(0, maxLength);
    if (st.length <= 0) {
        var i = 0;
        while (true) {
            i += 1;
            var new_st = String(i);
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
    var m = h1Start.exec(s);
    if (h1Start.test(s) && (m.length > 2)) {
        var title = m[1];
        title = title.split("§")[0]; // silently remove attempt to set short_title in H1
        s = m[2];
    } else {
        return "Must start with H1 heading to set title";
        /*raise InvalidWikiStructure('Must start with H1 heading to set title')*/
    }
    writeln("________________________");
    title = title.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    title = title.substring(0, 150);
    writeln("title: "+title);
    writeln("short_title: "+shortTitle);
    var node = new Object();
    node['title'] = title.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    node['short_title'] = shortTitle;
    node['children'] = [];

    /* do we need a StructureNode or will a TextNode do? */
    if (!(generalH.test(s))) {
        /* Text Node */
        node['text'] = s.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
        return node
    } /* else: StructureNode */

    /* determine used header depth: */
    var level = 0;
    for(var i= 2; i<7; i++) {
        m = new RegExp(getHeadingMatcher(i));
        if (m.test(s)) {
            level = i;
            writeln("Level ist "+level);
            break;
        }
    }

    /* leading text is used to set text of structure node */
    node['text'] = s.replace(m,'').replace(/^\s+|\s+$/g, '');
    writeln("Text saved: "+node['text']);

    do {
        writeln("Child section No. "+(node['children'].length+1)+" ____________");
        var splitDoc = m.exec(s);
        writeln("SplitDoc ("+splitDoc+")");
        writeln("s is ("+s+")");
        title = splitDoc[1].replace(/^\s+|\s+$/g, '');
        writeln("  title: "+title);
        if (splitDoc[2] == undefined) {
            shortTitle = turnIntoValidShortTitle(title,[],20);
        } else {
            shortTitle = turnIntoValidShortTitle(splitDoc[2].replace(/^\s+|\s+$/g, ''),[],20);
        }
        writeln("  shortTitle: "+shortTitle);
        s = splitDoc[4];
        var textParts = new RegExp("^(?:([^=].*?)(?:={"+level+"}|$)|())").exec(s);
        writeln(level);
        writeln(s);
        var text = textParts[1].replace(/=+$/, '').replace(/^\s+|\s+$/g, '');
        //var text = s.replace(m).replace(/^\s+|\s+$/g, '');
        writeln("  text: "+text);
        node['children'].push(parseStructure("= "+title+" =\n"+ s.replace(m, '').replace(/^\s+|\s+$/g, ''),shortTitle));
    } while (m.test(s));
    writeln("done");
    return node;
}

ClassParser.prototype.parse = function(text){
    return "<p>Not Implemented!</p>";
};

