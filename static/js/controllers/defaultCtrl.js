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

findecoApp.controller('FindecoDefaultCtrl',
    function ($scope, $location, $controller, $interval, Backend, Fesettings, GraphData, Navigator, User) {

        $scope.nav = Navigator;
        $scope.user = User;
        $scope.fesettings = Fesettings;
        $scope.allExpanded = false;
        $scope.showArguments = false;
        $scope.showMicroblogging = false;
        $scope.isTextLoaded = false;

        $scope.paragraphList = [];
        $scope.nodeInfo = {};
        $scope.nodeInfo.indexList = [];
        $scope.authors = [];
        $scope.sections = [];

        $scope.relocate = function (target) {
            $location.path(target + '/' + $scope.nav.nodePath);
        };

        $scope.markNode = Backend.markNode;

        $scope.markMainNode = function (markType, nodePath) {
            return Backend.markNode(markType, nodePath).success(function () {
                GraphData.loadGraphData($scope.nav.nodePath, $scope.graphType);
            });
        };

        $scope.updateNode = function () {
            $scope.isLoadingNode = true;
            Backend.loadNode($scope.nodeInfo, $scope.nav.nodePath).success(function (d) {
                $scope.allExpanded = true;
                $scope.authors = $scope.nodeInfo.authors;
                $scope.nav.nodeID = $scope.nodeInfo.nodeID;
                $scope.sections = $scope.nodeInfo.indexList;
                for (var i in $scope.sections) {
                    var indexNode = $scope.sections[i];
                    $scope.allExpanded = false;
                    indexNode.paragraphs = [];
                    indexNode.path = $scope.nav.getPathForNode(indexNode.shortTitle, indexNode.index);
                    indexNode.isLoaded = false;
                    indexNode.isExpanded = false;
                }
                $scope.isLoadingNode = false;

            });
        };

        $scope.expandAll = function () {
            for (var i = 0; i < $scope.sections.length; ++i) {
                $scope.expandSection($scope.sections[i]);
            }
            $scope.allExpanded = true;
        };

        $scope.collapseAll = function () {
            for (var i = 0; i < $scope.sections.length; ++i) {
                $scope.collapseSection($scope.sections[i]);
            }
            $scope.allExpanded = false;
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
            $scope.allExpanded = true;

            for (var i = 0; i < $scope.sections.length; ++i) {
                $scope.allExpanded &= $scope.sections[i].isExpanded
            }

        };

        $scope.collapseSection = function (section) {
            section.isExpanded = false;
            $scope.allExpanded = false;
        };

        $scope.isLoading = function () {
            return $scope.isLoadingNode;
        };

        $scope.updateNode();
    });
