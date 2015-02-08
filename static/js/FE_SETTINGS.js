/****************************************************************************************
 * Copyright (c) 2013 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
 *                                                                                      *
 * This file is part of Findeco.                                                        *
 *                                                                                      *
 * Findeco is free software; you can redistribute it and/or modify it under             *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * Findeco is distributed in the hope that it will be useful, but WITHOUT ANY           *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * Findeco. If not, see <http://www.gnu.org/licenses/>.                                 *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

/* Here you can set your Frontend settings. Please be aware that this file may be overwritten on Git updates.
 We suggest to store it outside
  */

angular.module('FindecoSettings', [])
    .constant('Version', '0.5.0')
    .constant('ActivatedLanguages', ['de-DE', 'en-EN', 'jp-JP'])
    .constant('Greetingbox', {
        enabled: true
    })
    .constant('Sidebar',{
        enable: false
    })
    .constant('Disclaimer',{
        text: 'Die Texte wurden von einzelnen Benutzern eingestellt und sind keine offizielle Aussage des Betreibers' ,
        enable: true
    })
    .constant('Boxes',{
        1:{
           title:'Was ist das?',
           content:'Dies ist eine Findeco Instanz. Findeco ist eine Online-Diskussionsplattform, die Diskussionen mit großen Nutzergruppen strukturiert. ',
           link:'http://www.findeco.de/extern/was-ist-findeco/',
           link_title:'mehr... (findeco.de)'
        },
        2:{
           title:'Wie funktionierts?',
           content:'Zur Zeit arbeiten wir an der Hilfe, Tutorials und Videoanleitungen. Der beste Einstieg ist zur Zeit die Hilfe. Wir bieten aber auch Workshops an, wenn du einen organisieren möchtest, melde dich bei uns..',
           link:'http://www.findeco.de/hilfe/',
           link_title:'zur Hilfe (findeco.de)'
        },
        3:{
           title:'RSS-Feeds (Extern)',
           content:'<ul> <li><a target="_new" href="http://www.findeco.de/category/allgemein/" title="Alle unter Allgemein abgelegten Beiträge ansehen">Findeco allgemein</a> <a  href="http://www.findeco.de/category/allgemein/feed/"><img style="height:15px" src="/static/images/feed.png" alt="Feed für alle unter Allgemein abgelegten Beiträge" /></a>	</li>        	<li class="cat-item cat-item-2"><a target="_new" href="http://www.findeco.de/category/entwicklung/" title="Alle unter Entwicklung abgelegten Beiträge ansehen">Findeco Entwicklung</a> <a href="http://www.findeco.de/category/entwicklung/feed/"><img style="height:15px" src="/static/images/feed.png" alt="Feed für alle unter Entwicklung abgelegten Beiträge" /></a></li>		<li class="cat-item cat-item-3"><a target="_new" href="http://www.findeco.de/category/systembetrieb-rlp/" title="Alle unter piraten-rlp.de abgelegten Beiträge ansehen">Systembetrieb findeco.piraten-rlp.de</a> <a href="http://www.findeco.de/category/systembetrieb-rlp/feed/"><img style="height:15px" src="/static/images/feed.png" alt="Feed für alle unter piraten-rlp.de abgelegten Beiträge" /></a></li>		<li class="cat-item cat-item-9"><a target="_new" href="http://www.findeco.de/category/systembetrieb-demo/" title="Alle unter Systembetrieb demo.findeco.de abgelegten Beiträge ansehen">Systembetrieb demo.findeco.de</a> <a href="http://www.findeco.de/category/systembetrieb-demo/feed/"><img style="height:15px" src="/static/images/feed.png" alt="Feed für alle unter Systembetrieb demo.findeco.de abgelegten Beiträge" /></a></li>	</ul>Feeds mit Systeminhalten stehen nach Anmeldung zur Verfügung.' ,
           link:'',
           link_title:''
        },
        4:{
           title:'Systemnews',
           content:'',
           link:'',
           special:'news'
        },
        5:{
           title:'Unser Manifest',
           content:'Findeco lebt von deinen Ideen und deiner Mitarbeit. Ein paar Grundsätze dazu findest du in unserem Manifest. ',
           link:'http://www.findeco.de/extern/unser-manifest/',
           link_title:'mehr... (findeco.de)'
        },
        6:
        {
           title:'Support',
           content:'Wir bauen zur Zeit unser Supportsystem auf. Unten findest du den Link zur Hilfe. bleiben Fragen kannst du uns unter Serverbetrieb@manano.de erreichen. ',
           link:'http://www.findeco.de/hilfe/',
           link_title:'zur Hilfe (findeco.de)'
        }})
    .factory('Fesettings', function (Disclaimer, Boxes, Version, Sidebar, Greetingbox, ActivatedLanguages) {
        var settings = {};
        settings.version = Version;
        settings.disclaimer = Disclaimer;
        settings.boxes = Boxes;
        settings.sidebar = Sidebar;
        settings.greetingbox = Greetingbox;
        settings.activatedLanguages = ActivatedLanguages;
        return settings;
    });
