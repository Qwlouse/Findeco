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

function ClassHelper() {}

var Helper = new ClassHelper();

ClassHelper.prototype.argumentClickHandler = function() {
    Main.loadText($(this).attr('data-path'));
};

ClassHelper.prototype.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

ClassHelper.prototype.getCSRFToken = function() {
    return Helper.getCookie('csrftoken');
}

ClassHelper.prototype.getActionFromUrl = function(url) {
    return url.substring(0,url.indexOf('/'));
};

ClassHelper.prototype.getId = function(string) {
    var search = /(\d+)/;
    var result = search.exec(string);
    if ( result == null ) {
        return null;
    }
    return parseInt(result[1]);
};

ClassHelper.prototype.getTargetPathFromUrl = function(url) {
    return url.substring(url.indexOf('/'));
};

ClassHelper.prototype.objectLength = function(object) {
    var i = 0;
    for ( o in object ) {
        i++;
    }
    return i;
};

ClassHelper.prototype.timestampToDate = function(time) {
    var d = new Date();
    d.setTime(time*1000);
    return d.toLocaleTimeString() + ', ' + d.toLocaleDateString(); 
};

ClassHelper.prototype.titleClickHandler = function() {
    if ( $(this).attr('data-path') == undefined ) {
        Controller.loadIndexRelative($(this).attr('data-shortTitle') + '.' + $(this).attr('data-index'));
    } else {
        Controller.loadIndex($(this).attr('data-path'));
    }
};

