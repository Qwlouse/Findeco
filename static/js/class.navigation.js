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

function ClassNavigation() {}
var Navigation = new ClassNavigation();

ClassNavigation.prototype.load = function (position) {
    left.empty();
    navigation.empty();
    
    if ( position == '/' ) {        
        return;
    }
    
    var tmp = position.split('/');
    Navigation.elements = {'boxes':{},'buttons':{}};
    
    var path = '';
    for ( var i = 0 ; i < tmp.length ; i++ ) {
        if ( path.substring(path.length-1) != '/' ) {
            path += '/';
        }
        path += tmp[i];
        if ( i < tmp.length - 1 ) {
            Navigation.elements['boxes'][path] = BoxRegister.newBox();
            Navigation.elements['boxes'][path].show('swap',left);
        
            DataRegister.get(Navigation.show,'index',path);
        }
        if ( i > 0 ) {
            $('<li class="button" style="z-index: 501; position: relative;" data-path="' + path + '"></li>')
                .click(function() {
                    var path = $(this).attr('data-path');
                    Controller.loadIndex(path);
                })
                .appendTo(navigation);
        }
    }
};

ClassNavigation.prototype.show = function (data) {
    // console.log('ClassNavigation','show');
    var info = data.getInfo();
    Navigation.elements['boxes'][info['path']].printData(data);
};

ClassNavigation.prototype.updateButtons = function () {
    // console.log('ClassNavigation','updateButtons');
    var buttons = navigation.children();
    for ( var b in buttons ) {
        if ( isNaN(b) ) {
            continue;
        }
        var path = buttons[b].getAttribute('data-path');
        var title = DataRegister.getTitle(path);
        if ( title == undefined ) {
            continue;
        }
        buttons[b].innerHTML = title;
    }
};