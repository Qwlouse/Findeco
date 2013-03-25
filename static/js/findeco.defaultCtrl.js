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

function FindecoDefaultCtrl($scope, $location, Backend) {
    $scope.path = THELocatoooooooor.getSanitizedPath();

    $scope.isTextLoaded = false;

    $scope.graphData = [];
    $scope.indexList = [];
    $scope.paragraphList = [];
    $scope.nodeInfo = [];

    $scope.getPath = function (p) {
        return THELocatoooooooor.getSanitizedPath(p);
    };

    $scope.relocate = function (target) {
        $location.path(target + '/' + THELocatoooooooor.getSanitizedArgumentFreePath());
    };

    $scope.parse = function (text, shortTitle) {
        return Parser.parse(text, shortTitle, true);
    };

    $scope.markNode = function (nodePath, markTypeInteger) {
        var markType = "follow";
        if (markTypeInteger == 2) {markType = "unfollow";}
        Backend.markNode(nodePath, markType).success(function () {
            for (var i = 0; i < $scope.paragraphList.length; i++) {
                if ($scope.paragraphList[i].path == nodePath) {
                    if (markTypeInteger == 2) {
                        $scope.paragraphList[i].isFollowing = 0;
                    } else {
                        $scope.paragraphList[i].isFollowing = 2;
                    }
                }
            }
        });
    };

    $scope.relocateRelativeTo = function (shortTitle, index) {
        var path = $scope.path;
        if ($scope.path == '/') {
            path = '';
        }
        $location.path(THELocatoooooooor.getSanitizedPath(shortTitle + '.' + index));
    };

    $scope.updateParagraphList = function () {
        Backend.loadText($scope.paragraphList, $scope.path).success(function () {
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateGraph = function () {
        Backend.loadGraphData($scope.graphData, $scope.path).success(function(data) {
            $scope.graphData = data.loadGraphDataResponse.graphDataChildren;
        });
    };

    $scope.updateNode = function () {
        Backend.loadNode($scope.nodeInfo, $scope.path)
    };

    $scope.initialize = function() {
        if ( THELocatoooooooor.isArgumentPath() ) {
            //$scope.updateParagraphList();
        } else {
            $scope.updateNode();
            $scope.updateGraph();
        }
    };
    $scope.initialize();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'Backend'];