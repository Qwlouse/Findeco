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

function ClassController() {}
var Controller = new ClassController();

ClassController.prototype.getPosition = function() {
    return Controller.position.replace(/\/$/g,'');
};

ClassController.prototype.load = function(element) {
    if ( element.id == 'imprint' ) {
        loadImprint();
    }
    if ( element.id == 'content' ) {
        loadPosition();
    }
};

ClassController.prototype.loadArguments = function() {
    Main.loadArguments(Controller.position);
}
ClassController.prototype.loadText = function() {
    Main.loadText(Controller.position);
}

ClassController.prototype.loadIndex = function(target) {
    Controller.position = target;
    document.location.hash = Controller.position;
}

ClassController.prototype.loadIndexRelative = function(target) {
    if ( Controller.position.substring(Controller.position.length-1) != '/' ) {
        Controller.position += '/';
    }
    Controller.position += target;
    document.location.hash = Controller.position;
}

ClassController.prototype.parentPosition = function() {
    var pos = Controller.position.lastIndexOf('/');
    if ( pos == -1 ) {
        return Controller.position;
    }
    return Controller.position.substring(0,pos + 1);
};

ClassController.prototype.position = '/';

ClassController.prototype.stateHandler = function(event) {
    // TODO: Mockup legacy, remove or comment out after testing is done.
    if ( parseInt(document.location.hash.substring(1)) >= 0 || parseInt(document.location.hash.substring(1)) <= 100 ) {
        return;
    }
    
    if ( Controller.position != document.location.hash.substring(1) ) {
         Controller.position = document.location.hash.substring(1);
    }
    // console.log('ClassController','stateHandler',event,document.location.hash);
    Microblogging.load(Controller.position);
    Navigation.load(Controller.position);
    Main.load(Controller.position);
}
