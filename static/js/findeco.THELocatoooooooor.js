/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim                         *
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

/**
 * Created with JetBrains PhpStorm.
 * User: justus
 * Date: 19.03.13
 * Time: 16:01
 * Yes, I'm fucking serious.
 */

function theLocatoooooooor() {
}

var THELocatoooooooor = new theLocatoooooooor();

theLocatoooooooor.prototype.getPath = function () {
    // We're going to hell for this. Sorry folks.
    var path = (document.location.hash + '/').match(/([_A-z]+\.\d+(\.(pro|con|neut)\.\d+)?\/)+/g);
    if (path == null || path.length == 0) {
        path = '/';
    } else {
        path = path[0];
    }
    return path;
}

function isNonEmpty(element, index, array) {
    return (element != "");
}

theLocatoooooooor.prototype.getPathParts = function () {
    var path = this.getPath();
    var pathParts = this.getPath().split("/").filter(isNonEmpty);
    return pathParts;
};

theLocatoooooooor.prototype.getSanitizedPath = function (target) {

    if (target == undefined) {
        target = '';
    } else {
        target = target.replace(/\//g, '');
    }

    var parts = this.getPathParts();
    var tmp = [];
    for (p in parts) {
        if (parts[p] == "") {
            continue;
        }
        tmp.push(parts[p]);
    }

    var sanePath = this.saneSlashAppending(tmp.join('/')) + target;
    if (sanePath != '/') {
        sanePath = this.removeTrailingSlashes(sanePath);
    }
    return sanePath;
};

theLocatoooooooor.prototype.getSanitizedArgumentFreePath = function () {
    var tmp = this.getSanitizedPath();
    if ( !this.isArgumentPath(tmp) ) {
        return tmp;
    }
    tmp = tmp.replace(/\.(pro|con|neut)\.\d+$/,'');
    return tmp;
}

theLocatoooooooor.prototype.removeTrailingSlashes = function (string) {
    if (string.substr(string.length-1) == '/') {
        string = string.substr(0, string.length - 1);
    }
    return string;
};

theLocatoooooooor.prototype.isArgumentPath = function (path) {
    var pP;
    if ( path == undefined ) {
        pP = this.getSanitizedPath().split(".");
    } else {
        pP = path.split(".");
    }
    var shortTitle = pP[pP.length - 2];
    if ( shortTitle == "pro"
        || shortTitle == "neut"
        || shortTitle == "con" ) {
        return true;
    }
    return false;
}

theLocatoooooooor.prototype.saneSlashAppending = function (string) {
    if (string.substr(string.length-1) != '/') {
        string += '/';
    }
    return string;
};
