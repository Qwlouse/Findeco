/****************************************************************************************
 * Copyright (c) 2012 Klaus Greff, Johannes Merkert, Maik Nauheim, Justus Wingert       *
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
    if (Math.abs(source.x - target.x) < 1e-6) {
        var b = 0;
    } else {
        var ratio = Math.abs((source.y - target.y) / (source.x - target.x));
        b = r/Math.sqrt(ratio * ratio + 1);
    }
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
    if (Math.abs(source.x - target.x) < 1e-6) {
        var ratio = 1;
        var b = r;
    } else {
        ratio = Math.abs((source.y - target.y) / (source.x - target.x));
        b = r/Math.sqrt(ratio * ratio + 1);
    }

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

findecoApp.directive('findecoGraph', function(GraphData, Navigator) {
    //------------------/ Parameters /--------------//
    var svg_minHeight = 150;
    var node_radius = 20;
    var node_innerRadius = 14;
    var link_distance = 80;

    // colors are like this [active.newFollow, active.follow, active.unfollow,
    //                   inactive.newFollow, inactive.follow, inactive.unfollow]
    var pie_chart_colors = ["#ffffff", "#999999", "#333333",
                            "#eeeeee", "#BBBBBB", "#555555"];
    var scale = d3.scale.log() // scaling of follows to node-size
        .domain([1, 100])
        .range([1, 2])
        .clamp(true);
    var pie = d3.layout.pie() // the pie layout for the nodes
        .sort(null);
    var arc = d3.svg.arc()    // the arc for the pie layout
        .outerRadius(node_radius)
        .innerRadius(node_innerRadius);


    //------------------/ Directive /--------------//
    return {
        restrict : 'A',
        scope: {
        },
        template:
            '<svg>' +
                '<defs>' +
                    '<marker class="arrowHead" orient="auto" markerHeight="5" markerWidth="5" refX="5" viewBox="0 -5 10 10" id="ArrowHead">' +
                        '<path d="M0,-5L10,0L0,5"></path>' +
                    '</marker>' +
                '</defs>'+
                '<defs>'+
                    '<filter id="blur">'+
                        '<feGaussianBlur stdDeviation="2"></feGaussianBlur>'+
                    '</filter>'+
                '</defs>'+
                '<g id="links"></g>' +
                '<g id="nodes"></g>' +
            '</svg>' +
            '<div id="tooltip" style="position: absolute; top: 0px; left: 0px; visibility: hidden;"></div> ',

        link : function (scope, element /*, attr*/) {
            scope.nodes = GraphData.nodes;

            var svg = d3.select(element[0].children[0])
                .attr('height', GraphData.svg_height)
                .attr('width', GraphData.svg_width);

            var tooltip = d3.select(element[0].children[1]);

            scope.$watchCollection('nodes', function (nodes) {
                // start the force layout
                var force = d3.layout.force()
                    .charge(-300)
                    .size([GraphData.svg_width, GraphData.svg_height])
                    .linkDistance(link_distance)
                    .nodes(nodes)
                    .links(GraphData.links)
                    .start();

                // add the links first so they will be underneath the nodes
                var link = svg.select('#links').selectAll(".link")
                    .data(GraphData.links);

                link.enter().append("line")
                    .attr("class", "link")
                    .attr("marker-end", "url(#ArrowHead)");

                link.exit().remove();
                // add a svg:group for all nodes
                var node = svg.select('#nodes').selectAll(".nodeGroup")
                    .data(nodes);

                var nodegroup = node.enter().append("g")
                    .call(force.drag)
                    .on("mouseover", function(d){
                        tooltip.html("<b>" + d.title + "</b>" +
                        	"<br/>Follows Gesamt: <span id='followsColorBox'> " + d.follows + "</span>" +
                            "<br/>direkt: <span id='directFollowColorBox'>" + d.newFollows + "</span>"+
                            "<br/>vererbt: <span id='transitiveFollowColorBox'>" + (d.follows - d.newFollows) + "</span>"+
                            "<br/>Entfolgungen: <span id='unfollowColorBox'>" + d.unFollows + "</span>");
                        return tooltip.style("visibility", "visible");
                    })
                    .on("mousemove", function(d){return tooltip.style("top", ((d.y + node_radius * scale(d.follows) )+ "px")).style("left",((d.x + node_radius * scale(d.follows))+ "px"));})
                    .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
                    .attr("class", function (d) {
                        if (d.path == Navigator.nodePath) {
                            return "nodeGroup";
                        }
                        else return "nodeGroup inactive";
                    });

                nodegroup.append("circle")  // shadow
                    .attr("r", node_radius)
                    .attr("class", "nodeShadow")
                    .attr("filter", "url(#blur)")
                    .attr('transform', "translate(2, 2)");

                var diff_button_group = nodegroup.append("svg:a")  // diff-button
                    .attr("xlink:href", function (d) {return '/diff/' + scope.path + '?compare=' + d.path; })
                    .append("g")
                    .attr('transform', "translate(-" + (node_radius-3) + ", -" + (node_radius-3) + ")");


                diff_button_group
                    .append("circle")
                    .attr("r", 13)
                    .attr("class", "diffButton")
                    .on('click', function() {alert('ha!');});

                diff_button_group
                    .append("text")
                    .attr("text-anchor", "middle")
                    .attr("class", "diffButtonText")
                    .text('diff');

                var g = nodegroup.append("g").append("svg:a")  // Node Center Group
                  .attr("xlink:href", function (d) {return '/' + d.path; });

                g.append("circle")  // Center Circle
                    .attr("class", function (d) {
                        if (d.path == Navigator.nodePath) return "active nodeBackgroundCircle";
                        else return "nodeBackgroundCircle";
                    })
                    .attr("r", node_radius);

                g.append("text")  // Node number
                    .attr("class", function (d) {
                        if (d.path == Navigator.nodePath) return "active nodeLabel";
                        else return "nodeLabel";
                    })
                    .attr("dy", ".35em")
                    .attr("text-anchor", "middle")
                    .text(function(d) {           // display only index as text
                        var s = d.path.split(".");
                        return s[s.length - 1]; });

                nodegroup.selectAll("path")
                    .data(function(d) {
                        if (d.path == Navigator.nodePath) {
                            return pie([ d.newFollows, d.follows - d.newFollows, d.unFollows, 0, 0, 0]);
                        } else {
                            return pie([ 0, 0, 0, d.newFollows, d.follows - d.newFollows, d.unFollows]);
                        }
                    })
                    .enter().append("svg:path")
                    .attr("d", arc)
                    .attr("r", 100)
                    .style("fill", function(d, i) {return pie_chart_colors[i];});

                node.exit().remove();

                force.on("tick", function() {
                    var svg_height_new = GraphData.svg_height;
                    nodegroup.attr('transform', function(d) {
                        var r = node_radius * scale(d.follows);
                        // make sure nodes don't exit the sides or the top
                        d.x = Math.max(Math.min(d.x, GraphData.svg_width - r - 5), r + 1);
                        d.y = Math.max(d.y, r + 1);
                        if (d.y + r + 5 > svg_height_new)  {
                            svg_height_new += Math.min(d.y + r  + 5 - GraphData.svg_height, 5);

                        }
                        return  'translate(' + d.x + ',' + d.y + ')' + ' scale(' + scale(d.follows) + ')';
                    });
                    if (GraphData.svg_height > svg_minHeight) {
                        svg_height_new -= 1;
                    }
                    if (svg_height_new != GraphData.svg_height) {
                        GraphData.svg_height = svg_height_new;
                        force.size([GraphData.svg_width, GraphData.svg_height]);
                        svg.attr("height", GraphData.svg_height);
                    }

                    // modify the links and the nodes
                    link.attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y;
                        })
                        .attr("x2", function(d) { return endx(d.source, d.target, node_radius * scale(d.target.follows) + 5)})
                        .attr("y2", function(d) { return endy(d.source, d.target, node_radius * scale(d.target.follows) + 5)});


                });
            });
        }
    }
});
