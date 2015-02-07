/****************************************************************************************
 * Copyright (c) 2014 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
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

'use strict';
angular.module('FindecoNavigatorService', [])
    .factory('Navigator', function ($rootScope, $location, Message) {
        var nodePattern = "[a-zA-Z][a-zA-Z0-9_-]{0,19}\\.[0-9]+";
        // TODO: disallow duplicated slashes.
        var rootPath = new RegExp("^/*$");
        var createPath = new RegExp("/+create/(proposal|argument)/(" + nodePattern + "/+)*(" + nodePattern + ")/*$");
        var nodePath = new RegExp("/+(" + nodePattern + "/+)*(" + nodePattern + ")/*$");
        var argumentPath = new RegExp("/+(" + nodePattern + "/+)*(" + nodePattern + ")\\.(pro|neut|con)\\.[0-9]+/*$");
        var userPath = new RegExp("^/user/[a-zA-Z][a-zA-Z0-9-_]{0,19}/*$");

        function isNonEmpty(element, index, array) {
            return (element != "");
        }

        var location = {
            path        : "",  // the full path but duplicate slashes are removed
            nodePath    : "",  // only the node path (parent for arguments, empty for users)
            argumentPath: "",  // the full path to the argument or node if it isn't an argument
            userName    : "",  // user
            parts       : [],
            entries     : [],  // contains objects with name and path for every ancestor node
            type        : "/"  // contains the path prefix or '/' or 'node' or 'argument'
        };

        function normalizeSlashes(path) {
            return path.split("/").filter(isNonEmpty).join('/');
        }

        location.updatePath = function () {
            Message.clear();
            var path = $location.path();
            location.segments = $location.search();
            location.parts = path.split("/").filter(isNonEmpty);
            location.path = '/' + location.parts.join("/");
            location.nodePath = "";
            location.argumentPath = "";
            location.userName = "";
            location.entries = [];
            location.type = "";
            // find out the type of path
            if (path.match(rootPath)) {
                location.type = "/";
            } else if (location.parts.length == 1 && location.parts[0] == 'index') {
                location.type = 'index';
            } else if (path.match(createPath)) {
                location.type = "create";
                location.nodePath = normalizeSlashes(nodePath.exec(location.path)[0]);
                location.argumentPath = location.nodePath
            } else if (path.match(nodePath)) {
                location.type = "node";
                location.nodePath = normalizeSlashes(nodePath.exec(location.path)[0]);
                location.argumentPath = location.nodePath
            } else if (path.match(argumentPath)) {
                location.type = "argument";
                location.argumentPath = normalizeSlashes(argumentPath.exec(location.path)[0]);
                location.nodePath = normalizeSlashes(location.argumentPath.replace(/\.(pro|con|neut)\.\d+\/?$/, ''));
            } else if (path.match(userPath)) {
                location.type = "user";
                location.userName = location.parts[1];
            }  else {
                location.type = "other";
            }
            // calculate entries
            var nodes = location.nodePath.split('/');
            var pathSoFar = "";
            for (var i = 0; i < nodes.length; ++i) {
                pathSoFar += '/' + nodes[i];
                location.entries.push({name: nodes[i], path: pathSoFar});
            }
            if (location.type == 'argument') {
                nodes = location.argumentPath.split('/');
                var arg_parts = nodes[nodes.length - 1].split('.');
                location.entries.push({name: arg_parts[2] + '.' + arg_parts[3], path: location.argumentPath});
            }
        };
        location.getPathForNode = function (shortTitle, index) {
            return normalizeSlashes(location.nodePath + '/' + shortTitle + '.' + index);
        };
        location.getPathForArgument = function (argType, index) {
            return normalizeSlashes(location.nodePath + '.' + argType + '.' + index);
        };
        location.getPathForUser = function (username) {
            return 'user/' + username;
        };
        location.changePath = function (newPath) {
            $location.path(newPath);
        };
        location.updatePath();
        $rootScope.$on('$routeChangeSuccess', location.updatePath);
        return location;
    });