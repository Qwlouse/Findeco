/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim                         *
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
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

'use strict';
/* Controllers */

function FindecoNavigationCtrl($scope) {
    $scope.calculateNavigationEntries = function () {
        var pathParts = THELocatoooooooor.getPathParts();
        var navEntries = [];
        var pathSoFar = "/#";

        var tmp = "";
        for (var i = 0; i < pathParts.length; ++i) {
            tmp = pathParts[i].split('.');
            pathSoFar += '/' + tmp[0] + '.' + tmp[1];
            navEntries.push({name: tmp[0] + '.' + tmp[1], path: pathSoFar});
        }
        if (THELocatoooooooor.isArgumentPath()) {
            pathSoFar += '.' + tmp[2] + '.' + tmp[3];
            navEntries.push({name: tmp[0] + '.' + tmp[1] + '.' + tmp[2] + '.' + tmp[3], path: '/#/argument' + pathSoFar.substr(2)});
        }
        return navEntries;
    }

    $scope.navigationEntries = $scope.calculateNavigationEntries();

    $scope.$on('$locationChangeSuccess', function (event, newLoc, oldLoc) {
        $scope.navigationEntries = $scope.calculateNavigationEntries();
    });
}

FindecoNavigationCtrl.$inject = ['$scope', '$location'];