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

function ClassMain() {}
var Main = new ClassMain();


ClassMain.prototype.isTypeLoaded = function (type) {
    if ( Main.loaded[type] == true ) {
        return true;
    }
    return false;
};

ClassMain.prototype.load = function (position) {
    // console.log('ClassMain','load');
    DataRegister.get(this.show,'index',position,true);
};

ClassMain.prototype.loadArguments = function (position) {
    // console.log('ClassMain','loadArguments');
    DataRegister.get(Main.append,'argument',position,true);
};

ClassMain.prototype.loadGraphData = function (position) {
    // console.log('ClassMain','loadArguments');
    if ( position == undefined ) {
        position = Controller.position;
    }
    DataRegister.get(Main.append,'graphdata',position,true);
};

ClassMain.prototype.loadText = function (position) {
    // console.log('ClassMain','loadText');
    DataRegister.get(Main.append,'text',position,true);
};

ClassMain.prototype.reset = function () {
    Main.loaded = {};
};

ClassMain.prototype.show = function (data) {
    // console.log('ClassMain','show');
    Main.reset();
    center.empty();
    Main.append(data);
    Main.loadGraphData();
};

ClassMain.prototype.append = function (data) {
    // console.log('ClassMain','append');
    Main.loaded[data.getType()] = true;
    
    if ( data.getType() == 'index'
        && data.json.loadIndexResponse != undefined 
        && Helper.objectLength(data.json.loadIndexResponse) == 0 ) {
        Controller.loadText();
    } else {
        var l = 0;
        for ( j in data.json ) {
            l += Helper.objectLength(data.json[j]);
        }
        if ( l > 0 ) {
            center.printData(data);
        }
    }
};
