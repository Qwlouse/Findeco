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
angular.module('FindecoGraphDataService', [])
    .factory('GraphData', function ($http) {
        var graphData = [];

        graphData.nodesEqual = function (nodeA, nodeB) {
            return nodeA.path == nodeB.path; // TODO: Use ID instead of path
        };

        graphData.updateNode = function (node, newNode) {
            node.authorGroup = newNode.authorGroup;
            node.follows     = newNode.follows;
            node.spamFlags   = newNode.spamFlags;
            node.unFollows   = newNode.unFollows;
            node.newFollows  = newNode.newFollows;
            node.title       = newNode.title;
            node.originGroup = newNode.originGroup;
            return node;
        };

        graphData.updateGraphData = function (data) {
            var loadedGraph = data.loadGraphDataResponse.graphDataChildren;

            var index = graphData.length;
            while (index--){
                var node = graphData[index];
                var nodeFound = false;
                var loadedNodeIndex = loadedGraph.length;
                while (loadedNodeIndex--) {
                    var loadedNode = loadedGraph[loadedNodeIndex];
                    if (graphData.nodesEqual(node, loadedNode)) {
                        loadedGraph.splice(loadedNodeIndex, 1);
                        graphData.updateNode(node, loadedNode);
                        nodeFound = true;
                        break;
                    }
                }
                if (!nodeFound) {
                    graphData.splice(index, 1);
                }
            }
            angular.forEach(loadedGraph, function (loadedNode) {
                graphData.push(loadedNode);
            });
        };

        graphData.loadGraphData = function (path, graphType) {
            if (graphType == undefined) {
                graphType = "full";
            }
            var url = ['/.json_loadGraphData', graphType, path].join('/');
            url = url.replace("//", "/");
            var promise = $http.get(url);
            promise.success(graphData.updateGraphData);
            return promise;
        };

        return graphData;
    });