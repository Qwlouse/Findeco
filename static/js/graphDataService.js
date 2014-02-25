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
    .factory('GraphData', function ($http, Navigator) {
        var svg_width = 580;
        var svg_height = 180;

        var nodes = [];
        var links = [];

        var graphData = {
            nodes: nodes,
            links: links
        };


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
            var index = nodes.length;
            while (index--){
                var node = nodes[index];
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
                    nodes.splice(index, 1);
                }
            }

            // add new nodes and set initial position
            for (var i = 0; i < loadedGraph.length; i++) {
                node = loadedGraph[i];
                node.x = svg_width/2 + 10 * i * Math.pow(-1, i);
                node.y = svg_height/2 + i;
                nodes.push(node);
            }

            // map paths to nodes
            var node_map = d3.map({});
            for (i = 0; i < nodes.length; i++) {
                nodes[i].active = false;
                node_map.set(nodes[i].path, nodes[i]);
            }
            // currently selected node is active
            if (node_map.has(Navigator.nodePath)) {
                node_map.get(Navigator.nodePath).active = true;
            }
            // construct the links
            links.length = 0;
            for (i = 0; i < nodes.length; i++) {
                node = nodes[i];
                for (var j = 0; j < node.originGroup.length; j++) {
                    links.push({"source": node_map.get(node.originGroup[j]), "target": node});
                }
            }
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