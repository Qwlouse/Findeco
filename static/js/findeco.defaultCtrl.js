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

function FindecoDefaultCtrl($scope, $location, Backend, User, Navigator) {
    $scope.nav = Navigator;
    $scope.user = User;

    $scope.allExpanded = false;

    $scope.isTextLoaded = false;

    $scope.graphData = [];
    $scope.paragraphList = [];
    $scope.nodeInfo = [];
    $scope.nodeInfo.indexList = [];
    $scope.nodeInfo.path = $scope.nav.argumentPath;
    $scope.sections = [];

    $scope.relocate = function (target) {
        $location.path(target + '/' + $scope.nav.nodePath);
    };

    $scope.markNode = Backend.markNode;


    $scope.updateGraph = function () {
        Backend.loadGraphData($scope.graphData, $scope.nav.nodePath).success(function (data) {
            $scope.graphData = data.loadGraphDataResponse.graphDataChildren;
            $scope.isLoadingGraph =false;
        });
    };

    $scope.updateNode = function () {
        Backend.loadNode($scope.nodeInfo, $scope.nav.argumentPath).success(function (d) {
            $scope.allExpanded = true;

            for (var i in $scope.nodeInfo.indexList) {
                var indexNode = $scope.nodeInfo.indexList[i];
                $scope.allExpanded = false;
                indexNode.paragraphs = [];
                indexNode.path = $scope.nav.getPathForNode(indexNode.shortTitle, indexNode.index);
                indexNode.isLoaded = false;
                indexNode.isExpanded = false;
            }
            $scope.isLoadingNode =false;
           
        });
    };

    $scope.expandAll = function () {
        var sections = $scope.nodeInfo.indexList;
        for (var i = 0; i < sections.length; ++i) {
            $scope.expandSection(sections[i]);
        }
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
        $scope.isLoadingNode =true;
        $scope.isLoadingGraph =true;
        $scope.updateNode();
        $scope.updateGraph();
       
    };
    $scope.isLoading = function (){
    	
    	if   (!($scope.isLoadingNode)&&!($scope.isLoadingGraph )){
    	    return false;
    	}else{
    		return true;
    	}
    	
    }
    $scope.initialize();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'Backend', 'User', 'Navigator'];