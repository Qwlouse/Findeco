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

ClassParser.prototype.errorState = false;

ClassParser.prototype.isErrorState = function() {
    return Parser.errorState;
}

ClassParser.prototype.parse = function(text, shortTitle){
    var wikiText = '';
    try {
        Parser.errorState = false;
        wikiText = convertSchemaToCreole(parseStructure(text, shortTitle));
    } catch (e) {
        Parser.errorState = true;
        wikiText = e;
    }
    var textDiv = document.createElement("div");
    textDiv.innerHTML = "";
    var creole = new Parse.Simple.Creole( {
        forIE: document.all,
        interwiki: {
            WikiCreole: 'http://www.wikicreole.org/wiki/',
            Wikipedia: 'http://en.wikipedia.org/wiki/'
        },
        linkFormat: ''
    } );
    creole.parse(textDiv,wikiText);
    return $('<div>' + textDiv.innerHTML + '<div>');
};