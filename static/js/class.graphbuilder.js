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
ClassGraphbuilder.prototype.createCircleStructure = function (title, id, type, consent) {
    var newText = document.createTextNode(title);
    var linkDIV = document.createElement("div");
    linkDIV.appendChild(newText);
    linkDIV.setAttribute("class", "linklike");
    var innerDIV = document.createElement("div");
    innerDIV.appendChild(linkDIV);
    innerDIV.setAttribute("class", "circle");
    innerDIV.setAttribute("onClick", "showNode(this.parentNode, true);");
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
    outerDIV.dbId = id;
    outerDIV.type = type;

    var data = [consent, 1.0-consent];

    var r = 40,
        h = 2*r,
        w = 2*r,
        color = ["#33ff33","#BB0000", "#0000ff"],
        donut = d3.layout.pie().sort(null),
        arc = d3.svg.arc().innerRadius(r - 20).outerRadius(r - 10);

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
    marker.setAttribute("refX", "13");
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
    outerArrow.spring = new ClassSpring(parentCircle.particle, childCircle.particle, 80.0);
    outerArrow.A = parentCircle;
    outerArrow.B = childCircle;
    return outerArrow
};


function initPage(anchorGraphData, navigationData, selected_id, doNodeUpdate) {
    document.getElementById('microblog').loading = false;
    document.getElementById("text").waitForText = selected_id;
    window.onscroll = reloadTest;
    if (document.getElementById('graph')) {
        document.getElementById('graph').paddingTop = 30.0;
        document.getElementById('graph').paddingLeft = 30.0;
        document.getElementById('graph').paddingRight = 30.0;
        document.getElementById('graph').paddingBottom = 30.0;
        buildAnchorGraph(JSON.parse(anchorGraphData));
        // get selected Node:
        var graphNode = document.getElementById('graph');
        for (var i = 0; i < graphNode.circles.length; ++i) {
            var node = graphNode.circles[i];
            if ((node.dbId == selected_id) && node.type != "Slot") {
                showNode(node, doNodeUpdate);
                break;
            }
        }
    } else {
        Dajaxice.microblogging.getAllActivities(showMicroblogging);
    }
    updateNavigation(JSON.parse(navigationData));
}


ClassGraphbuilder.prototype.buildAnchorGraph = function (data) {
    var Anchors = data["Anchors"];
    var graphNode = document.getElementById('graph');
    graphNode.stepRuns = false;
    while ( graphNode.firstChild ) graphNode.removeChild( graphNode.firstChild );
    graphNode.circles = [];
    graphNode.arrows = [];

    for (var i = 0; i < Anchors.length; ++i) {
        var anchor = Anchors[i];
        var anchor_circle = this.createCircleStructure(anchor['nr_in_parent'], anchor['id'], anchor['type'], anchor['consent']);
        anchor_circle.particle.x = i*80;
        anchor_circle.particle.targetX = i*80;
        anchor_circle.particle.targetForce = 0.05;
        graphNode.circles.push(anchor_circle);
        graphNode.appendChild(anchor_circle);
    }

    // add related nodes
    var relatedNodes = data['related_nodes'];
    for (i = 0; i < relatedNodes.length; ++i) {
        var node = relatedNodes[i];
        var node_circle = this.createCircleStructure(node['nr_in_parent'], node['id'], node['type'], anchor['consent']);
        node_circle.particle.y = -160;
        node_circle.particle.x = i*80;
        graphNode.circles.push(node_circle);
        graphNode.appendChild(node_circle);
    }

    // add connections
    var connections = data['connections'];
    for (i = 0; i < connections.length; ++i) {
        var connection = connections[i];
        var source_node = this.getNodeById(graphNode.circles, connection[0], "TextNode");
        var target_node = this.getNodeById(graphNode.circles, connection[1], "TextNode");
        var arrow = this.createArrowStructure(source_node, target_node);
        graphNode.arrows.push(arrow);
        graphNode.insertBefore(arrow, graphNode.firstChild);
    }
    if (!(graphNode.stepRuns)) {
        graphNode.stepRuns = true;
        this.step();
    }
};

ClassGraphbuilder.prototype.updateGraph = function (data) {
    var graphNode = document.getElementById('graph');
    var Anchors = JSON.parse(data["graph_data"])["Anchors"];
    // draw voting
    updateVoting(data["voting_data"]);

    var newCircles = [];
    for (var i = 0; i < Anchors.length; ++i) {
        var anchor = Anchors[i];
        var old_circle = this.getNodeById(graphNode.circles, anchor['id'], anchor['type']);
        var anchor_circle = this.createCircleStructure(anchor['nr_in_parent'], anchor['id'], anchor['type'], anchor['consent']);
        anchor_circle.particle.x = i*80;
        if (old_circle != -1) {
            anchor_circle.particle.x = old_circle.particle.x;
            anchor_circle.particle.y = old_circle.particle.y;
        }
        anchor_circle.particle.targetX = i*80;
        anchor_circle.particle.targetForce = 0.05;
        newCircles.push(anchor_circle);
    }

    // add related nodes
    var relatedNodes = JSON.parse(data["graph_data"])['related_nodes'];
    for (i = 0; i < relatedNodes.length; ++i) {
        var node = relatedNodes[i];
        var node_circle = this.createCircleStructure(node['nr_in_parent'], node['id'], node['type'], anchor['consent']);
        node_circle.particle.y = -160;
        node_circle.particle.x = i*80;
        old_circle = this.getNodeById(graphNode.circles, node['id'], node['type']);
        if (old_circle != -1) {
            node_circle.particle.x = old_circle.particle.x;
            node_circle.particle.y = old_circle.particle.y;
        }
        newCircles.push(node_circle);
    }
    // clear graphNode and (re-)insert nodes
    while ( graphNode.firstChild ) graphNode.removeChild( graphNode.firstChild );
    graphNode.circles = newCircles;
    for (i = 0; i < newCircles.length; ++i) {
        graphNode.appendChild(newCircles[i]);
    }

    // add connections
    var connections = JSON.parse(data["graph_data"])['connections'];
    for (i = 0; i < connections.length; ++i) {
        var connection = connections[i];
        var source_node = this.getNodeById(graphNode.circles, connection[0], "TextNode");
        var target_node = this.getNodeById(graphNode.circles, connection[1], "TextNode");
        var arrow = this.createArrowStructure(source_node, target_node);
        graphNode.arrows.push(arrow);
        graphNode.insertBefore(arrow, graphNode.firstChild);
    }
    if (!(graphNode.stepRuns)) {
        graphNode.stepRuns = true;
        step();
    }

    // mark centerCircle clicked
    var currentIndex = this.getIndexInCircles(graphNode.circles, data['id'], data['type']);
    var currentNode = graphNode.circles[currentIndex];
    currentNode.firstChild.nextSibling.nextSibling.firstChild.setAttribute("class", "");

    // reposition graph
    if (!(graphNode.stepRuns)) {
        graphNode.stepRuns = true;
        this.step();
    }
};


/////////////////////// Simulation /////////////////////////////////
ClassGraphbuilder.prototype.step = function () {
    var graphNode = document.getElementById('graph');
    var circles = graphNode.circles;
    var arrows = graphNode.arrows;
    var particles = [];
    for (var i = 0; i < circles.length; ++i)
        particles.push(circles[i].particle);
    var springs = [];
    for (i = 0; i < arrows.length; ++i)
        springs.push(arrows[i].spring);
    var particleMovement = this.updateParticles(particles, springs);

    // set new position
    for (i = 0; i < circles.length; ++i) {
        circles[i].style.left = Math.round(particles[i].x - circles[i].style.width / 2 - 30) + "px";
        circles[i].style.top = Math.round(particles[i].y - circles[i].style.height / 2) + "px";
    }
    // draw arrows
    for (i = 0; i < arrows.length; i++) {
        this.drawArrow(arrows[i]);
    }

    // adjust graph dimensions
    var minPosY = 0;
    var maxPosY = 0;
    var minPosX = 0;
    var maxPosX = 0;
    for (i = 0; i < particles.length; i++) {
        minPosY = Math.min(particles[i].y, minPosY);
        maxPosY = Math.max(particles[i].y, maxPosY);
        minPosX = Math.min(particles[i].x - 30, minPosX);
        maxPosX = Math.max(particles[i].x - 30, maxPosX);
    }
    var paddingRight = Math.max(maxPosX + 36, graphNode.paddingRight - 2);
    particleMovement += Math.abs(maxPosX + 36 - graphNode.paddingRight);
    graphNode.paddingRight = paddingRight;
    var paddingBottom = Math.max(maxPosY + 36, graphNode.paddingBottom - 2);
    particleMovement += Math.abs(maxPosY + 36 - graphNode.paddingBottom);
    graphNode.paddingBottom = paddingBottom;
    var paddingTop = Math.max(minPosY * -1 + 31, graphNode.paddingTop - 2);
    particleMovement += Math.abs(minPosY * -1 + 31 - graphNode.paddingTop);
    graphNode.paddingTop = paddingTop;
    var paddingLeft = Math.max(minPosX * -1 + 31, graphNode.paddingLeft - 2);
    particleMovement += Math.abs(minPosX * -1 + 31 - graphNode.paddingLeft);
    graphNode.paddingLeft = paddingLeft;
    graphNode.style.paddingRight = Math.round(paddingRight) + "px";
    graphNode.style.paddingBottom = Math.round(paddingBottom) + "px";
    graphNode.style.paddingTop = Math.round(paddingTop) + "px";
    graphNode.style.paddingLeft = Math.round(paddingLeft) + "px";
    //graphNode.style.width = Math.round(paddingRight+paddingLeft) + "px";
    //graphNode.style.height = Math.round(paddingTop+paddingBottom) + "px";
    // iterate
    if (particleMovement > 0.2) {
        setTimeout("this.step()", 25);
    } else {
        graphNode.stepRuns = false;
    }
};


/////////////////////// Drawing /////////////////////////////////
ClassGraphbuilder.prototype.drawArrow = function (arrowdiv) {
    var svg = arrowdiv.firstChild;
    var arrowLine = svg.firstChild.nextSibling;
    var particleA = arrowdiv.A.particle;
    var particleB = arrowdiv.B.particle;
    svg.setAttribute("width", Math.max(Math.round(Math.abs(particleB.x-particleA.x))+10,10));
    svg.setAttribute("height", Math.max(Math.round(Math.abs(particleB.y-particleA.y))+10,10));
    if (particleB.x - particleA.x < 0) {
        arrowLine.setAttribute("x2", "5");
        arrowLine.setAttribute("x1", particleA.x-particleB.x+5);
        //alert(arrowdiv.style.width);
        arrowdiv.style.left = Math.round(particleA.x - 28)+Math.round(particleB.x - particleA.x)-5+"px";
    } else {
        arrowLine.setAttribute("x1", "5");
        arrowLine.setAttribute("x2", particleB.x-particleA.x+5);
        arrowdiv.style.left = Math.round(particleA.x - 28 - 5)+"px";
    }
    if (particleB.y - particleA.y < 0) {
        arrowLine.setAttribute("y2", "5");
        arrowLine.setAttribute("y1", particleA.y-particleB.y+5);
        arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2)+Math.round(particleB.y - particleA.y)-5+"px";
    } else {
        arrowLine.setAttribute("y1", "5");
        arrowLine.setAttribute("y2", particleB.y-particleA.y+5);
        arrowdiv.style.top = Math.round(particleA.y - arrowdiv.style.height / 2 - 5)+"px";
    }
};


/////////////////////// Helpers ///////////////////////////////////////////////////
ClassGraphbuilder.prototype.getIndexInCircles = function (circles, id, type) {
    for (var i = 0; i < circles.length; i++) {
        if ((circles[i].dbId == id) && (circles[i].type == type)) return i;
    }
    return -1;
};

ClassGraphbuilder.prototype.getNodeById = function (circles, id, type) {
    for (var i = 0; i < circles.length; i++) {
        if ((circles[i].dbId == id) && (circles[i].type == type)) return circles[i];
    }
    return -1;
};
