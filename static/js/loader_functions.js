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
    //$(document).ajaxStart(function() {
      //  $('#loading').show();
    //});
    //$(document).ajaxStop(function() {
     //   $('#loading').hide();
   // });
    

 
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
    "topicList" : {"loadIndexResponse":[{"shortTitle":"topic","index":1,"fullTitle":"<h2>Wahlprogramm</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]},{"shortTitle":"topic","index":2,"fullTitle":"<h2>Grundsatzprogramm</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]},{"shortTitle":"topic","index":3,"fullTitle":"<h2>Satzung</h2>","authorGroup":[{"displayName":"author1"}]}]}
    ,"subTopicList" : {"loadIndexResponse":[{"shortTitle":"subtopic","index":1,"fullTitle":"<h2>Umwelt und Verbraucherschutz</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]},{"shortTitle":"subtopic","index":2,"fullTitle":"<h2>Wirtschaft</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}]}
    ,"subSubTopicList" : {"loadIndexResponse":[
        {"shortTitle":"subsubtopic","index":1,"fullTitle":"<h2>Nachhaltigkeit</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]}
        ,{"shortTitle":"subsubtopic","index":2,"fullTitle":"<h2>Energieversorgung</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"subsubtopic","index":3,"fullTitle":"<h2>Klimawandel</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"subsubtopic","index":4,"fullTitle":"<h2>Wasserwirtschaft</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ]}
    ,"subSubSubTopicList" : {"loadIndexResponse":[
        {"shortTitle":"subsubtopic","index":1,"fullTitle":"<h2>Trinkwasser</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]}
        ,{"shortTitle":"subsubtopic","index":2,"fullTitle":"<h2>Abwasser</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"subsubtopic","index":3,"fullTitle":"<h2>Gewässerschutz</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ]}
    ,"subSubSubSubTopicOverview" : {"loadTextResponse":{"paragraphs":[{"wikiText":"<h2>Abwasser</h2>Abwasser ist ein Wertstoff und wir streben einen ressourcenschonenden Umgang mit den wertvollen Inhaltsstoffen an. Wir treten für die Abschaffung des Anschlusszwanges für häusliche Abwässer an das Abwassernetz ein, wenn die Einhaltung der Ablaufparameter nach der EU-Rahmenrichtlinie eigenverantwortlich sichergestellt wird. Industrielle und die von Krankenhäusern stammende Abwässer sind geeignet vorzubehandeln. Vermischung mit häuslichen Abwässern ist zu vermeiden.","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}],"isFollowing":1}}
    ,"subSubSubTopicOverview" : {"loadTextResponse":{"paragraphs":[
        {"wikiText":"<h2>Trinkwasser</h2>Wasser ist ein kommunales Gut und muss jedem Bürger zur Verfügung stehen. Wir stehen für die Rekommunalisierung der Wasserversorgung ein, da sie als Infrastruktur der Grundversorgung dient. Wir streben eine hohe Trinkwasserqualität an und wollen diese auch durch die Reduzierung von Schadstoffeintrag erreichen. Die Trinkwasserverordnung soll an aktuelle Erkenntnisse über Wasserinhaltsstoffe regelmässig angepasst werden. Die Eigenwasserversorgung privater Haushalte soll grundsätzlich erlaubt sein. Sofern eine private Hauswasserversorgung möglich ist, lehnen wir einen Anschlusszwang an das kommunale Trinkwassernetz ab. Die Qualitätsprüfung ist eigenverantwortlich zu leisten. ","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"wikiText":"<h2>Abwasser</h2>Abwasser ist ein Wertstoff und wir streben einen ressourcenschonenden Umgang mit den wertvollen Inhaltsstoffen an. Wir treten für die Abschaffung des Anschlusszwanges für häusliche Abwässer an das Abwassernetz ein, wenn die Einhaltung der Ablaufparameter nach der EU-Rahmenrichtlinie eigenverantwortlich sichergestellt wird. Industrielle und die von Krankenhäusern stammende Abwässer sind geeignet vorzubehandeln. Vermischung mit häuslichen Abwässern ist zu vermeiden.","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"wikiText":"<h2>Gewässerschutz</h2>Die Wasserressourcen sind von Beeinträchtigungen freizuhalten. In allen Bereichen müssen Eingriffe in den Boden auf ihre Verträglichkeit mit dem Gewässerschutz hin überprüft und gegebenenfalls angepasst werden. ","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ],"isFollowing":1}}
    ,"subSubSubTopicArguments" : {"loadIndexResponse":[
        {"shortTitle":"pro","index":1,"fullTitle":"Absolut geil!","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]}
        ,{"shortTitle":"pro","index":2,"fullTitle":"Voll toll!","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]}
        ,{"shortTitle":"contra","index":1,"fullTitle":"Alle doof außer Mama!","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"neutral","index":1,"fullTitle":"Irgendwie fällt mir dazu nichts ein...","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ]}
    ,"imprint" : {"loadTextResponse":{"paragraphs":[{"wikiText":"=Impressum=\r\nAngaben gemäß § 5 TMG:\r\n\r\n\r\nKrohlas & Wingert IT GbR\r\n\r\nHauptstraße 91\r\n\r\n76706 Dettenheim\r\n\r\n\r\n\r\nVertreten durch: Sven Krohlas, Justus Wingert\r\n\r\nIhr Ansprechpartner für Fragen jeder Art: Justus Wingert (justus_wingert@web.de)","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}],"isFollowing":1}}
};














