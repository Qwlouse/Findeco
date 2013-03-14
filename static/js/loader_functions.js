/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert <justus_wingert@web.de>                            *
 *                                                                                      *
 * This file is part of BasDeM.                                                         *
 *                                                                                      *
 * BasDeM is free software; you can redistribute it and/or modify it under              *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * BasDeM is distributed in the hope that it will be useful, but WITHOUT ANY            *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/
 
/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

var left = BoxRegister.newBox();
var center = BoxRegister.newBox();
var right = BoxRegister.newBox();
var navigation = null;

var currentPosition = 0;
var endPosition = 0;

// window.onpopstate = Controller.stateHandler;
/** **************************************** **/
/** Here we should load all global instances **/
/** **************************************** **/

var Login = new ClassLogin();
var User=new ClassUser();
var Contribute = new ClassContribute();



$(document).ready(load);

function load(){
	

    navigation = $('#location');
    $('#logo').click(function(){ Controller.loadIndex('/'); } );
    

 
    left.show('left');
    center.show('center');
    right.show('right');
    Login.setLoginButtonState();
    $(window).bind('hashchange',Controller.stateHandler);
    
    if ( document.location.hash == '' ) {
        document.location.hash = '#/';
    } else {
        Controller.stateHandler();
    }
}

function loadImprint() {
    right.empty();
    center.empty();
    left.empty();
    navigation.empty();
    var data = new ClassData();
    data.load(jsonData.imprint);
    data.setInfo('text','/');
    center.printData(data);
}


var jsonData = {
    "imprint" : {"loadTextResponse":{"paragraphs":[{"wikiText":"=Impressum=\r\nAngaben gemäß § 5 TMG:\r\n\r\n\r\nKrohlas & Wingert IT GbR\r\n\r\nHauptstraße 91\r\n\r\n76706 Dettenheim\r\n\r\n\r\n\r\nVertreten durch: Sven Krohlas, Justus Wingert\r\n\r\nIhr Ansprechpartner für Fragen jeder Art: Justus Wingert (justus_wingert@web.de)","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}],"isFollowing":1}}
};














