/* Findeco is dually licensed under GPLv3 or later and MPLv2.
 #
 ################################################################################
 # Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>,
 # Klaus Greff <klaus.greff@gmx.net>
 # This file is part of Findeco.
 #
 # Findeco is free software; you can redistribute it and/or modify it under
 # the terms of the GNU General Public License as published by the Free Software
 # Foundation; either version 3 of the License, or (at your option) any later
 # version.
 #
 # Findeco is distributed in the hope that it will be useful, but WITHOUT ANY
 # WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 # A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License along with
 # Findeco. If not, see <http://www.gnu.org/licenses/>.
 ################################################################################
 #
 ################################################################################
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/.
 ##############################################################################*/

function ClassGraphbuilder() {}

var Graphbuilder = new ClassGraphbuilder();

/////////////////////// Graph Construction /////////////////////////////////
ClassGraphbuilder.prototype.createCircleStructure = function (path, newFollows, follows, unFollows, originGroup) {
    var pathParts = path.split('.');
    var title = pathParts[pathParts.length-1];
    var newText = document.createTextNode(title);
    var linkDIV = document.createElement("div");
    linkDIV.appendChild(newText);
    linkDIV.setAttribute("class", "linklike");
    var innerDIV = document.createElement("div");
    innerDIV.appendChild(linkDIV);
    innerDIV.setAttribute("class", "circle");
    innerDIV.setAttribute("onClick", "Controller.loadIndex('/"+path+"');"); // Link to path would be better...
    var outerDIV = document.createElement("div");
    outerDIV.setAttribute("class", "masspoint");
    var diagramDIV = document.createElement("div");
    diagramDIV.setAttribute("class", "diagram_container");
    var whiteContainerDIV = document.createElement("div");
    var whitenerDIV = document.createElement("div");
    whitenerDIV.setAttribute("class", "whitener");
    whiteContainerDIV.appendChild(whitenerDIV);
    whiteContainerDIV.setAttribute("style", "width: 0; height: 0; overflow: visible;")
    outerDIV.appendChild(whiteContainerDIV);
    outerDIV.appendChild(diagramDIV);
    outerDIV.appendChild(innerDIV);
    outerDIV.particle = new ClassParticle();
    outerDIV.particle.targetY = 0.0;
    //outerDIV.setAttribute("id", "circle_"+title.replace(/^\s+|\s+$/g, ''));
    outerDIV.path = path;
    outerDIV.originGroup = originGroup;

    var data = [newFollows, follows-newFollows, unFollows];
    var modifier=0;
    if (Controller.position =="/"+path){
    	 modifier=  5;
    }
    
    var r = 30,
        h = 2*r,
        w = 2*r,
        color = ["#FF9900","#0066CC", "#999999"],
        donut = d3.layout.pie().sort(null),
        arc = d3.svg.arc().innerRadius(r - 20 + modifier).outerRadius(r - 10 );
       
        

    var svg = d3.select(diagramDIV).append("svg:svg")
        .attr("width", w)
        .attr("height", h)
        .attr("transform", "translate(-100, -50)")
        .append("svg:g")
        .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

    var arcs = svg.selectAll("path")
        .data(donut(data))
        .enter().append("svg:path")
        .attr("fill", function(d, i) { return color[i]; })
        .attr("d", arc)
        .each(function(d) { this._current = d; });
    //d3.select(svg).attr("transform", "translate(200,0)");

    return outerDIV;
};


ClassGraphbuilder.prototype.createArrowStructure = function (parentCircle, childCircle) {
    //create arrow svg
    var svgDocument = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgDocument.setAttribute("version", "1.2");
    svgDocument.setAttribute("width", "10");
    svgDocument.setAttribute("height", "10");
    var defsTag = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    var marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");
    marker.setAttribute("refX", "5");
    marker.setAttribute("refY", "0");
    marker.setAttribute("id", "arrow");
    marker.setAttribute("orient", "auto");
    marker.setAttribute("style", "overflow:visible;");
    var markerPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    markerPath.setAttribute("d", "M -1,-3 7,0 -1,3 0,0 z");
    markerPath.setAttribute("fill", "black");
    markerPath.setAttribute("transform", "scale(0.5)");
    marker.appendChild(markerPath);
    defsTag.appendChild(marker);
    svgDocument.appendChild(defsTag);
    var arrowLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    arrowLine.setAttribute("x1", "0");
    arrowLine.setAttribute("y1", "0");
    arrowLine.setAttribute("x2", "10");
    arrowLine.setAttribute("y2", "0");
    arrowLine.setAttribute("stroke", "black");
    arrowLine.setAttribute("stroke-width", "3");
    arrowLine.setAttribute("style", "marker-end:url(#arrow)");
    svgDocument.appendChild(arrowLine);
    //create container
    var outerArrow = document.createElement("div");
    outerArrow.setAttribute("class", "fixpoint");
    outerArrow.appendChild(svgDocument);
    outerArrow.spring = new ClassSpring(parentCircle.particle, childCircle.particle, 50.0);
    outerArrow.A = parentCircle;
    outerArrow.B = childCircle;
    return outerArrow
};


ClassGraphbuilder.prototype.getConnections = function (nodes) {
    var connections = [];
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        for (var j = 0; j < node.originGroup.length; j++) {
            for (var k = 0; k < nodes.length; k++) {
                if (nodes[k].path == node.originGroup[j]) {
                    var newConnection = {'sourceNodePath': node.originGroup[j], 'targetNodePath': node.path};
                    connections.push(newConnection);
                }
            }
        }
    }
    return connections;
};


ClassGraphbuilder.prototype.buildAnchorGraph = function (data, graphNode) {
    this.graphNode = graphNode;
    var Anchors = data['graphDataChildren'];
    this.stepRuns = false;
    while ( graphNode.firstChild ) graphNode.removeChild( graphNode.firstChild );
    this.circles = [];
    this.arrows = [];

    for (var i = 0; i < Anchors.length; ++i) {
        var anchor = Anchors[i];
        var anchor_circle = this.createCircleStructure(anchor['path'], anchor['newFollows'], anchor['follows'], anchor['unFollows'], anchor['originGroup']);
        anchor_circle.particle.x = i*50;
        anchor_circle.particle.targetX = i*50;
        anchor_circle.particle.targetForce = 0.05;
        this.circles.push(anchor_circle);
        graphNode.appendChild(anchor_circle);
    }

    // add related nodes
    var relatedNodes = data['graphDataRelated'];
    for (i = 0; i < relatedNodes.length; ++i) {
        var node = relatedNodes[i];
        var node_circle = this.createCircleStructure(node['path'], node['newFollows'], node['follows'], node['unFollows'], node['originGroup']);
        node_circle.particle.y = -100;
        node_circle.particle.x = i*50;
        this.circles.push(node_circle);
        graphNode.appendChild(node_circle);
    }

    // add connections
    var connections = this.getConnections(this.circles);
    for (i = 0; i < connections.length; ++i) {
        var connection = connections[i];
        var sourceNode = this.getNodeByPath(this.circles, connection['sourceNodePath']);
        var targetNode = this.getNodeByPath(this.circles, connection['targetNodePath']);
        var arrow = this.createArrowStructure(sourceNode, targetNode);
        this.arrows.push(arrow);
        graphNode.insertBefore(arrow, graphNode.firstChild);
    }
    if (!(this.stepRuns)) {
        this.stepRuns = true;
        step();
    }
};


ClassGraphbuilder.prototype.updateGraph = function (data) {
    var Anchors = data["graphDataChildren"];
    // draw voting
    ////updateVoting(data["voting_data"]);

    var newCircles = [];
    for (var i = 0; i < Anchors.length; ++i) {
        var anchor = Anchors[i];
        var old_circle = this.getNodeByPath(this.circles, anchor['path']);
        var anchor_circle = this.createCircleStructure(anchor['path'], anchor['newFollows'], anchor['follows'], anchor['unFollows'], anchor['originGroup']);
        anchor_circle.particle.x = i*50;
        if (old_circle != -1) {
            anchor_circle.particle.x = old_circle.particle.x;
            anchor_circle.particle.y = old_circle.particle.y;
        }
        anchor_circle.particle.targetX = i*50;
        anchor_circle.particle.targetForce = 0.05;
        newCircles.push(anchor_circle);
    }

    // add related nodes
    var relatedNodes = JSON.parse(data["graph_data"])['related_nodes'];
    for (i = 0; i < relatedNodes.length; ++i) {
        var node = relatedNodes[i];
        var node_circle = this.createCircleStructure(node['path'], node['newFollows'], node['follows'], node['unFollows'], node['originGroup']);
        node_circle.particle.y = -100;
        node_circle.particle.x = i*50;
        old_circle = this.getNodeByPath(this.circles, node['path']);
        if (old_circle != -1) {
            node_circle.particle.x = old_circle.particle.x;
            node_circle.particle.y = old_circle.particle.y;
        }
        newCircles.push(node_circle);
    }
    // clear graphNode and (re-)insert nodes
    while ( this.graphNode.firstChild ) this.graphNode.removeChild( this.graphNode.firstChild );
    this.circles = newCircles;
    for (i = 0; i < newCircles.length; ++i) {
        this.graphNode.appendChild(newCircles[i]);
    }

    // add connections
    var connections = JSON.parse(data["graph_data"])['connections'];
    for (i = 0; i < connections.length; ++i) {
        var connection = connections[i];
        var source_node = this.getNodeByPath(this.circles, connection[0]);
        var target_node = this.getNodeByPath(this.circles, connection[1]);
        var arrow = this.createArrowStructure(source_node, target_node);
        this.arrows.push(arrow);
        this.graphNode.insertBefore(arrow, this.graphNode.firstChild);
    }
    if (!(this.stepRuns)) { // TODO: This part is repeated below. This seems stupid.
        this.stepRuns = true;
        this.step();
    }

    // mark centerCircle clicked
    var currentIndex = this.getIndexInCircles(this.circles, data['path']);
    var currentNode = this.circles[currentIndex];
    currentNode.firstChild.nextSibling.nextSibling.firstChild.setAttribute("class", "");

    // reposition graph
    if (!(this.stepRuns)) {
        this.stepRuns = true;
        step();
    }
};


/////////////////////// Simulation /////////////////////////////////
function step() {
    var graphNode = Graphbuilder.graphNode;
    var circles = Graphbuilder.circles;
    var arrows = Graphbuilder.arrows;
    var particles = [];
    for (var i = 0; i < circles.length; ++i)
        particles.push(circles[i].particle);
    var springs = [];
    for (i = 0; i < arrows.length; ++i)
        springs.push(arrows[i].spring);
    var particleMovement = updateParticles(particles, springs);

    // set new position
    for (i = 0; i < circles.length; ++i) {
        circles[i].style.left = Math.round(particles[i].x - circles[i].style.width / 2 - 20) + "px";
        circles[i].style.top = Math.round(particles[i].y - circles[i].style.height / 2) + "px";
    }
    // draw arrows
    for (i = 0; i < arrows.length; i++) {
        Graphbuilder.drawArrow(arrows[i]);
    }

    // adjust graph dimensions
    var minPosY = 0;
    var maxPosY = 0;
    var minPosX = 0;
    var maxPosX = 0;
    for (i = 0; i < particles.length; i++) {
        minPosY = Math.min(particles[i].y, minPosY);
        maxPosY = Math.max(particles[i].y, maxPosY);
        minPosX = Math.min(particles[i].x - 20, minPosX);
        maxPosX = Math.max(particles[i].x - 20, maxPosX);
    }
    var paddingRight = Math.max(maxPosX + 24, graphNode.paddingRight - 2);
    particleMovement += Math.abs(maxPosX + 24 - graphNode.paddingRight);
    graphNode.paddingRight = paddingRight;
    var paddingBottom = Math.max(maxPosY + 24, graphNode.paddingBottom - 2);
    particleMovement += Math.abs(maxPosY + 24 - graphNode.paddingBottom);
    graphNode.paddingBottom = paddingBottom;
    var paddingTop = Math.max(minPosY * -1 + 21, graphNode.paddingTop - 2);
    particleMovement += Math.abs(minPosY * -1 + 21 - graphNode.paddingTop);
    graphNode.paddingTop = paddingTop;
    var paddingLeft = Math.max(minPosX * -1 + 21, graphNode.paddingLeft - 2);
    particleMovement += Math.abs(minPosX * -1 + 21 - graphNode.paddingLeft);
    graphNode.paddingLeft = paddingLeft;
    graphNode.style.paddingRight = Math.round(paddingRight) + "px";
    graphNode.style.paddingBottom = Math.round(paddingBottom) + "px";
    graphNode.style.paddingTop = Math.round(paddingTop) + "px";
    graphNode.style.paddingLeft = Math.round(paddingLeft) + "px";
    //graphNode.style.width = Math.round(paddingRight+paddingLeft) + "px";
    //graphNode.style.height = Math.round(paddingTop+paddingBottom) + "px";
    // iterate
    if (particleMovement > 0.2) {
        setTimeout("step()", 25);
    } else {
        Graphbuilder.stepRuns = false;
    }
}


/////////////////////// Drawing /////////////////////////////////
ClassGraphbuilder.prototype.drawArrow = function (arrowdiv) {
    var svg = arrowdiv.firstChild;
    var arrowLine = svg.firstChild.nextSibling;
    var particleA = arrowdiv.A.particle;
    var particleB = arrowdiv.B.particle;
    svg.setAttribute("width", String(Math.max(Math.round(Math.abs(particleB.x-particleA.x))+10,10)));
    svg.setAttribute("height", String(Math.max(Math.round(Math.abs(particleB.y-particleA.y))+10,10)));
    if (particleB.x - particleA.x < 0) {
        arrowLine.setAttribute("x2", "5");
        arrowLine.setAttribute("x1", String(particleA.x-particleB.x+5));
        //alert(arrowdiv.style.width);
        arrowdiv.style.left = Math.round(particleA.x - 28)+Math.round(particleB.x - particleA.x)-5+"px";
    } else {
        arrowLine.setAttribute("x1", "5");
        arrowLine.setAttribute("x2", String(particleB.x-particleA.x+5));
        arrowdiv.style.left = Math.round(particleA.x - 28 - 5)+"px";
    }
    if (particleB.y - particleA.y < 0) {
        arrowLine.setAttribute("y2", "5");
        arrowLine.setAttribute("y1", String(particleA.y-particleB.y+5));
        arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2)+Math.round(particleB.y - particleA.y)-3+"px";
    } else {
        arrowLine.setAttribute("y1", "5");
        arrowLine.setAttribute("y2", String(particleB.y-particleA.y+5));
        arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2 - 3)+"px";
    }
};


/////////////////////// Helpers ///////////////////////////////////////////////////
ClassGraphbuilder.prototype.getIndexInCircles = function (circles, path) {
    for (var i = 0; i < circles.length; i++) {
        if (circles[i].path == path) return i;
    }
    return -1;
};

ClassGraphbuilder.prototype.getNodeByPath = function (circles, path) {
    for (var i = 0; i < circles.length; i++) {
        if (circles[i].path == path) return circles[i];
    }
    return -1;
};
