/****************************************************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim, Johannes Merkert       *
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

function FindecoArgumentCtrl($scope, $location, $routeParams, Backend, User, TMP) {
    $scope.tmp = TMP;
    $scope.user = User;

    $scope.isArgument = true;

    $scope.markNode = Backend.markNode;

    $scope.nodeInfo = [];

    $scope.path = locator.getSanitizedArgumentFreePath();
    $scope.argumentPath = locator.getSanitizedPath();

    $scope.isTextLoaded = false;
    $scope.argumentList = [];

    $scope.getPath = function () {
        return locator.getSanitizedArgumentFreePath();
    };

    $scope.parse = function(text,shortTitle) {
        if ( text == undefined || text == "" ) {
            return '';
        }
        return Parser.parse(text,shortTitle,true);
    };

    $scope.relocateRelativeTo = function(shortTitle,index) {
        var path = $scope.path;
        if ( $scope.path == '/' ) {
            path = '';
        }
        $location.path(locator.getSanitizedPath(shortTitle + '.' + index));
    };

    $scope.updateParagraphList = function() {
    };

    $scope.relocateToDerivate = function() {
        $location.path($scope.nodeInfo.derivate);
    };

    function amendArguments() {
        for (var i = 0; i < $scope.argumentList.length; ++i) {
            var arg = $scope.argumentList[i];
            arg.path = locator.getPathForArgument(arg.argType, arg.index);
        }
    }

    $scope.updateArgument = function () {
        Backend.loadText($scope.nodeInfo, $scope.argumentPath).success( function (d) {
            if ( $scope.nodeInfo.path != undefined && $scope.nodeInfo.path != '' ) {
                $scope.nodeInfo[0].derivate = $scope.nodeInfo.path;
            }
            $scope.nodeInfo = $scope.nodeInfo[0];
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateArgumentList = function () {
        Backend.loadArgument($scope.argumentList , $scope.path).success(amendArguments);
    };

    $scope.updateArgumentList();
    if ( locator.isArgumentPath() ) {
        $scope.updateArgument();
    }
}

FindecoArgumentCtrl.$inject = ['$scope', '$location', '$routeParams', 'Backend', 'User', 'TMP'];