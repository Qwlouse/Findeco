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

function ClassDataRegister() {this.register = new function() {};}
var DataRegister = new ClassDataRegister();


ClassDataRegister.prototype.data = {'index':{},'text':{},'microblogging':{},'argument':{}};

ClassDataRegister.prototype.get = function(callback,type,position,force) {
    // console.log('ClassDataRegister','get',force);
    if ( DataRegister.data[type][position] == undefined
        || force != undefined ) {
        DataRegister.load(callback,type,position);
        return;
    }
    var data = new ClassData();
    data.setInfo(type,position);
    data.load(DataRegister.data[type][position]);
    callback(data);
}

ClassDataRegister.prototype.getTitle = function(path) {
    return this.title[path];
}

ClassDataRegister.prototype.handleAjax = function(json) {
    var action = Helper.getActionFromUrl(this.url);
    var position = Helper.getTargetPathFromUrl(this.url);
    
    var type = '';
    
    switch ( action ) {
        case '.json_loadIndex': 
            type = 'index';
            if ( position.substring(0,5) == '/True' ) {
                type = 'argument';
                position = position.substring(5);
            }
        break;
        case '.json_loadMicroblogging':
            type = 'microblogging'; 
            position = position.replace(/\/(newer|older)/g,'');
            position = position.replace(/\/\d+/g,'');
        break;
        case '.json_loadText': type = 'text'; break;
    }
    // console.log(type,position,DataRegister.data[type]);
    var callbacks = DataRegister.data[type][position];
    
    DataRegister.data[type][position] = json;
    
    var data = new ClassData();
    data.setInfo(type,position);
    data.load(DataRegister.data[type][position]);
    
    // console.log(data,callbacks);
    
    for ( c in callbacks ) {
        if ( c == 'next' ) {
            continue;
        }
        // console.log(callbacks,c);
        callbacks[c](data);
    }
    
    // Necessary call to ensure that Navigation Buttons are allways filled!
    Navigation.updateButtons();
}

ClassDataRegister.prototype.load = function(callback,type,position) {
    // console.log('ClassDataRegister','load');
    // Storing the callback reference into the data object for future reference.
    if ( typeof DataRegister.data[type][position] != 'object' 
        || DataRegister.data[type][position].next == undefined ) {
        DataRegister.data[type][position] = {'next':1,0:callback};
    } else {
        DataRegister.data[type][position][DataRegister.data[type][position].next++] = callback;
        return;
    }
    
    var loadType = '';
    
    switch ( type ) {
        case 'index': loadType = '.json_loadIndex'; break;
        case 'microblogging': $.get('.json_loadMicroblogging/newer' + position,DataRegister.handleAjax,'json'); return;
        case 'argument': $.get('.json_loadIndex/True' + position,DataRegister.handleAjax,'json'); return;
        case 'text': loadType = '.json_loadText'; break;
    }
    
    $.get(loadType + position,DataRegister.handleAjax,'json');
}

ClassDataRegister.prototype.setTitle = function(path,title) {
    this.title[path] = title;
}

ClassDataRegister.prototype.title = {};
