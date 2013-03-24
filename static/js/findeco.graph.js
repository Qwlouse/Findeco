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

/////////////////////// Helpers ////////////////////////////////////////////////
/**
 * Helper function that calculates the x value of an endpoint of a line such
 * that it ends at the border of the target node instead of at the center.
 * @param source starting point of the line (should have source.x and source.y)
 * @param target end-point of the line (should have target.x and target.y)
 * @param r the radius of the circle at target
 * @return {int} the x value of the endpoint of the line
 */
function endx(source, target, r) {
    var ratio = Math.abs((source.y - target.y) / (source.x - target.x));
    var b = r/Math.sqrt(ratio * ratio + 1);
    if ((source.x - target.x) > 0) {
        return target.x + b;
    } else {
        return target.x - b;
    }
}

/**
 * Helper function that calculates the y value of an endpoint of a line such
 * that it ends at the border of the target node instead of at the center.
 * @param source starting point of the line (should have source.x and source.y)
 * @param target end-point of the line (should have target.x and target.y)
 * @param r the radius of the circle at target
 * @return {int} the y value of the endpoint of the line
 */
function endy(source, target, r) {
    var ratio = Math.abs((source.y - target.y) / (source.x - target.x));
    var b = r/Math.sqrt(ratio * ratio + 1);
    if ((source.y - target.y) > 0) {
        return target.y + ratio * b;
    } else {
        return target.y - ratio * b;
    }
}


//////////////////// findeco-graph Directive ///////////////////////////////////
/*
    <div findeco-graph data="data"></div>
*/

findecoApp.directive('findecoGraph', function( ) {
    // Parameters
    var svg_width = 580,
        svg_height = 150;
    var node_radius = 20;

    // colors are like this [active.newFollow, active.follow, active.unfollow,
    //                   inactive.newFollow, inactive.follow, inactive.unfollow]
    var pie_chart_colors = ["#ffffff", "#999999", "#333333",
                            "#eeeeee", "#BBBBBB", "#555555"];
    var scale = d3.scale.log() // scaling of follows to node-size
        .domain([1, 1000])
        .range([1, 2])
        .clamp(true);
    var pie = d3.layout.pie() // the pie layout for the nodes
        .sort(null);
    var arc = d3.svg.arc()    // the arc for the pie layout
        .outerRadius(node_radius)
        .innerRadius(14);

    return {
        restrict : 'A',
        scope: {
            data: '=',
            path: '='
        },

        link : function (scope, element, attrs) {
            // create svg container
            var svg = d3.select(element[0])
                .append("svg")
                .attr("width", svg_width)
                .attr("height", svg_height);

            // add arrowhead
            var defs = svg.append("svg:defs");
            var marker = defs.append("svg:marker")
                .attr("id", "ArrowHead")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 5)
                .attr("markerWidth", 5)
                .attr("markerHeight", 5)
                .attr("orient", "auto")
                .attr("class", "arrowHead")
                .append("svg:path")
                .attr("d", "M0,-5L10,0L0,5");

            var filter = svg.append("svg:defs")
                .append("svg:filter")
                .attr("id", "blur")
                .append("svg:feGaussianBlur")
                .attr("stdDeviation", 2);

            scope.$watch('data', function (nodes) {
                if (nodes == undefined) {
                    return;
                }
                var links = [];
                // map paths to nodes
                var node_map = d3.map({});
                for (var i = 0; i < nodes.length; i++) {
                    node_map.set(nodes[i].path, nodes[i]);
                    nodes[i].active = false;
                }
                // currently selected node is active
                if (node_map.has(scope.path)) {
                    node_map.get(scope.path).active = true;
                }
                // construct the links
                for (i = 0; i < nodes.length; i++) {
                    var n = nodes[i];
                    for (var j = 0; j < n.originGroup.length; j++) {
                        links.push({"source": node_map.get(n.originGroup[j]), "target": n});
                    }
                }

                // set initial position of nodes
                for (i = 0; i < nodes.length; i++) {
                    nodes[i].x = 100 + 70 * i;
                    nodes[i].y = svg_height - 80 + i;
                }

                // start the force layout
                var force = d3.layout.force()
                    .charge(-300)
                    .gravity(0)
                    .size([svg_width, svg_height])
                    .linkDistance(80)
                    .nodes(nodes)
                    .links(links)
                    .start();

                // add the links first so they will be underneath the nodes
                var link = svg.selectAll(".link")
                    .data(links)
                    .enter().append("line")
                    .attr("class", "link")
                    .attr("marker-end", "url(#ArrowHead)");

                // add a svg:group for all nodes
                var node = svg.selectAll(".node")
                    .data(nodes)
                    .enter().append("g")
                    .attr("class", "nodeGroup")
                    .attr("title", function (d) { return d.path; })
                    .call(force.drag)
                    .append("svg:a")
                    .attr("xlink:href", function (d) {return '/#/' + d.path; });

                node.append("circle")  // shadow
                    .attr("r", node_radius)
                    .attr("class", "nodeShadow")
                    .attr("filter", "url(#blur)")
                    .attr('transform', "translate(2, 2)");


                node.append("circle")
                    .attr("class", function (d) {
                        if (d.active) return "active nodeBackgroundCircle";
                        else return "nodeBackgroundCircle";
                    })
                    .attr("r", node_radius);


                node.append("text")
                    .attr("class", function (d) {
                        if (d.active) return "active nodeLabel";
                        else return "nodeLabel";
                    })
                    .attr("dy", ".35em")
                    .attr("text-anchor", "middle")
                    .text(function(d) {           // display only index as text
                        var s = d.path.split(".");
                        return s[s.length - 1]; });

                node.selectAll("path")
                    .data(function(d) {
                        if (d.active) {
                            return pie([ d.newFollows, d.follows - d.newFollows, d.unFollows, 0, 0, 0]);
                        } else {
                            return pie([ 0, 0, 0, d.newFollows, d.follows - d.newFollows, d.unFollows]);
                        }
                    })
                    .enter().append("svg:path")
                    .attr("d", arc)
                    .attr("r", 100)
                    .style("fill", function(d, i) {return pie_chart_colors[i];});


                force.on("tick", function(e) {
                    // push all nodes to a baseline position
                    var k = 0.2 * e.alpha;
                    nodes.forEach(function(o, i) {
                        o.y += (svg_height - 80 - o.y) * k;
                        o.x += (70*i + 80 - o.x) * k;
                    });

                    // modify the links and the nodes
                    link.attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y;
                        })
                        .attr("x2", function(d) { return endx(d.source, d.target, node_radius * scale(d.target.follows) + 5)})
                        .attr("y2", function(d) { return endy(d.source, d.target, node_radius * scale(d.target.follows) + 5)});

                    node.attr('transform', function(d) {  return  'translate(' + d.x + ',' + d.y + ')' + ' scale(' + scale(d.follows) + ')'; });
                });
            });
        }
    }
});
