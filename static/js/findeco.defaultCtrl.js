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

function FindecoDefaultCtrl($scope, $location, Backend, User) {
    $scope.path = locator.getSanitizedPath();
    $scope.isArgument = false;

    $scope.allExpanded = false;

    $scope.isTextLoaded = false;

    $scope.graphData = [];

    $scope.paragraphList = [];
    $scope.nodeInfo = [];
    $scope.nodeInfo.indexList = [];
    $scope.nodeInfo.path = $scope.path;
    $scope.sections = [];
    $scope.user = User;


    $scope.getPath = function (p) {
        return locator.getSanitizedPath(p);
    };

    $scope.relocate = function (target) {
        $location.path(target + '/' + locator.getSanitizedArgumentFreePath());
    };

    $scope.parse = function (text, shortTitle) {
        if (text != undefined) {
            return Parser.parse(text, shortTitle, true);
        } else {
            return "";
        }
    };

    $scope.markNode = Backend.markNode;

    $scope.relocateRelativeTo = function (shortTitle, index) {
        var path = $scope.path;
        if ($scope.path == '/') {
            path = '';
        }
        $location.path(locator.getSanitizedPath(shortTitle + '.' + index));
    };

    /*$scope.updateParagraphList = function () {
     Backend.loadText($scope.paragraphList, $scope.path).success(function () {
     $scope.isTextLoaded = true;
     });
     };*/

    $scope.updateGraph = function () {
        Backend.loadGraphData($scope.graphData, $scope.path).success(function (data) {
            $scope.graphData = data.loadGraphDataResponse.graphDataChildren;
        });
    };

    $scope.updateNode = function () {
        Backend.loadNode($scope.nodeInfo, $scope.path).success(function (d) {
            $scope.allExpanded = true;

            for (var i in $scope.nodeInfo.indexList) {
                $scope.allExpanded = false;
                $scope.nodeInfo.indexList[i].paragraphs = [];
                $scope.nodeInfo.indexList[i].path = locator.getPathForIndex($scope.nodeInfo.indexList[i].shortTitle, $scope.nodeInfo.indexList[i].index);
                $scope.nodeInfo.indexList[i].isLoaded = false;
                $scope.nodeInfo.indexList[i].isExpanded = false;
            }
        });
    };

    $scope.expandAll = function () {
        var tmp = [];
        Backend.loadText(tmp, locator.getSanitizedPath()).success(function (d) {
            if (d.loadTextResponse == undefined || d.loadTextResponse.paragraphs == undefined) {
                // TODO: Something went terribly wrong.
                return;
            }

            var paragraphs = d.loadTextResponse.paragraphs;

            // O(m*n) I certainly don't like it but don't see another way...
            for (var p in paragraphs) {
                for (var i in $scope.nodeInfo.indexList) {
                    var section = $scope.nodeInfo.indexList[i];
                    var path = locator.getPathForIndex(section.shortTitle, section.index);
                    if (paragraphs[p].path.substr(0,path.length) == path) {
                        section.paragraphs.push(paragraphs[p]);
                        section.isLoaded = true;
                        section.isExpanded = true;
                        section.path = path;
                        break;
                    }
                }
            }
            $scope.allExpanded = true;
        });
    };

    $scope.expandSection = function (section) {
        if (!section.isLoaded) {
            Backend.loadText(section.paragraphs, section.path).success(function (d) {
                section.isFollowing = d.loadTextResponse.isFollowing;
                section.isFlagging = d.loadTextResponse.isFlagging;
                section.isLoaded = true;
                section.isExpanded = true;
            });
        } else {
            section.isExpanded = true;
        }

    };

    $scope.collapseSection = function (section) {
        section.isExpanded = false;
    };

    $scope.initialize = function () {
        if (locator.isArgumentPath()) {
            //$scope.updateParagraphList();
        } else {
            $scope.updateNode();
            $scope.updateGraph();
        }
    };
    $scope.initialize();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'Backend', 'User'];