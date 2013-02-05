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
Parser.h1Start = "^\s*=(?P<title>[^=]+)=*\s*$";
Parser.generalH = "^\s*(={2,6}(?P<title>[^=]+)=*)\s*$";

ClassParser.prototype.parse = function (s, shortTitle){
    var m = s.match(self.h1Start);
    if(m.length > 1){
        var title = m[1]
        title = title.split("§")[0] /* silently remove attempt to set short_title in H1 */
        s = s.replace(self.h1Start,"");
    } else {
        return false;
        /*raise InvalidWikiStructure('Must start with H1 heading to set title')*/
    }
    title = title.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    title = title.substring(0,150)
    var node = new Array()
    node['title'] = title.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
    node['short_title'] = shortTitle;
    node['children'] = new Array();

    /* do we need a StructureNode or will a TextNode do? */
    if !(s.match(self.generalH).length <= 1) {
        /* Text Node */
        node['text'] = s.replace(/^\s+|\s+$/g, ''); /* strip in javascript */
        return node
    } /* else: StructureNode */
};