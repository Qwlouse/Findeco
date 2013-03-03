/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert <justus_wingert@web.de>                            *
 *                                                                                      *
 * This file is part of BasDeM.                                                         *
 *                                                                                      *
 * BasDeM is free software; you can redistribute it and/or modify it under              *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * BasDeM is distributed in the hope that it will be useful, but WITHOUT ANY            *
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

function ClassData(json) {
	this.load(json);
}

ClassData.prototype.rqhandler= RqHandler;
ClassData.prototype.getInfo = function() {
    return this.info;
};

ClassData.prototype.getJQueryObject = function() {
    return this.html;
};

ClassData.prototype.getType = function() {
    return this.info['type'];
};

ClassData.prototype.load = function(data) {
    this.json = data;
    
    this.html = $('<div>');
    this.html.addClass('innerContent');
    
    // console.log(data);
    
    for ( var d in data ) {
        if ( d == 'loadIndexResponse' ) {
            this.loadIndexResponse(data[d]);
        }
        if ( d == 'loadTextResponse' ) {
            this.loadTextResponse(data[d]);
        }
        if ( d == 'loadMicrobloggingResponse' ) {
            this.loadMicrobloggingResponse(data[d]);
        }
        if ( d == 'loadGraphDataResponse' ) {
            this.loadGraphDataResponse(data[d]);
        }
    }
};

ClassData.prototype.loadArgumentResponse = function(data) {
    this.type = 'argument';
    
    var procontra = $('<div>')
        .addClass('argprocontra')
        .appendTo(this.html);
    var arguments = {};
    arguments['pro'] = $('<ul>')
        .addClass('argpro')
        .appendTo(procontra);
    arguments['neut']= $('<ul>')
        .addClass('argneutral')
        .appendTo(this.html);
    arguments['con'] = $('<ul>')
        .addClass('argcontra')
        .appendTo(procontra);
    
    $('<br>').appendTo(procontra);
    
    for ( var d in data ) {
        var path = Controller.getPosition() + '.' + data[d].shortTitle + '.' + data[d].index;
        $('<li data-path="' + path + '">' + data[d].fullTitle + '</li>')
            .click(Helper.argumentClickHandler)
            .appendTo(arguments[data[d].shortTitle]);
    }
};

ClassData.prototype.loadGraphDataResponse = function(data) {
    this.type = 'graphdata';
    //alert(data['graphDataChildren'].length);
    //alert(data['graphDataChildren'][0]['path']);
    //alert(data['graphDataRelated'].length);
    var graphNode = document.createElement('div');
    var text = document.createTextNode("Hallo Graph!");
    graphNode.appendChild(text);
    graphNode.id = "graph";
    graphNode.paddingTop = 30.0;
    graphNode.paddingLeft = 30.0;
    graphNode.paddingRight = 30.0;
    graphNode.paddingBottom = 30.0;
    Graphbuilder.buildAnchorGraph(data, graphNode);
    $(graphNode).appendTo(this.html);
};

ClassData.prototype.loadIndexResponse = function(data) {
    this.type = 'index';
    
    for ( d in data ) {
        if ( data[d].shortTitle == 'pro'
            || data[d].shortTitle == 'neut'
            || data[d].shortTitle == 'con' ) {
            this.loadArgumentResponse(data); 
            return;
        }
        
        var absolutepath = '';
        if ( this.info != undefined && this.info.path != undefined ) {
            var parentpath = this.info.path;
            if ( parentpath.substring(parentpath.length-1) != '/' ) {
                parentpath += '/';
            }
            absolutepath = parentpath + data[d].shortTitle + '.' + data[d].index;
            DataRegister.setTitle(absolutepath,data[d].fullTitle);
            absolutepath = ' data-path="' + absolutepath + '"';
        }
        $('<h2 data-shortTitle="' + data[d].shortTitle + '" data-index="' + data[d].index + '"' + absolutepath + '>' + data[d].fullTitle + '</h2>')
            .appendTo(this.html)
            .click(Helper.titleClickHandler);
    }
};

ClassData.prototype.loadTextResponse = function(data) {
    this.type = 'text';
    var wikiText = "";
    var shortTitle = data['paragraphs'][0].path.replace(/(.*)\//g,'').replace(/.\d+$/,'');
    

    for ( var p in data['paragraphs'] ) {
        wikiText =  data['paragraphs'][p].wikiText + "\n";
        var parsed = Parser.parse(wikiText,shortTitle,true)
        
        //Adding View for Follow Unfollow
        
        if(data['paragraphs'][p].isFollowing==0){
        	var followContent = '<span class="followStar"><img src="static/images/star0.png" alt="Sie folgen dem Vorschlag nicht. Klicken sie zum folgen" title="Sie folgen dem Vorschlag nicht. Klicken sie zum folgen"></span>';
        	var followAction = 'follow';
        }
        if(data['paragraphs'][p].isFollowing==1){
        	var followContent = '<span class="followStar"><img src="static/images/star1.png" alt="Sie folgen dem Vorschlag transitiv. Klicken sie zum entfolgen" title="Sie folgen dem Vorschlag transitiv. Klicken sie zum entfolgen"></span>';
        	var followAction = 'unfollow';
        		
        }
        if(data['paragraphs'][p].isFollowing==2){
        	var followContent = '<span class="followStar"><img src="static/images/star2.png" alt="Sie folgen dem Vorschlag. Klicken sie zum entfolgen" title="Sie folgen dem Vorschlag. Klicken sie zum entfolgen"></span>';
        	var followAction = 'unfollow';
        }
        var followrqurl= String('.json_markNode/'+followAction+'/'+data['paragraphs'][p].path) ;
        
        if(data['paragraphs'][p].isFlagging==0) {
        	var spamContent = '<span class="spamFlag"><img src="static/images/star2.png" alt="Diesen Vorschlag als Spam markieren" title="Diesen Vorschlag als Spam markieren"></span>';
        	var spamAction = 'spam';
        }else{
        	var spamContent = '<span class="spamFlag"><img src="static/images/star1.png" alt="Spammarkierung entfernen" title="Spammarkierung entfernen"></span>';
        	var spamAction = 'notspam';
        }
        var spamrqurl= String('.json_markNode/'+spamAction+'/'+data['paragraphs'][p].path) ;
      
        
        var div ='<div><div class="followContainer" style="float:right">';
        div += followContent;
        div += spamContent;
        div +='</div>'+ parsed.innerHTML + '<div>';
        
       output=$(div);
        
        //<div><div style="float:right"><span class="FollowStar"><img src="static/images/star2.png" alt="Sie folgen dem Vorschlag. Klicken sie zum entfolgen" title="Sie folgen dem Vorschlag. Klicken sie zum entfolgen"></span></div>' + parsed.innerHTML + '<div>'
        
        
        output.find("span.followStar").click(RqHandler.get({   
    		url: followrqurl,
    		success:Controller.loadText
    	}));
       output.find("span.spamFlag").click(RqHandler.get({   
    		url: spamrqurl,
    		success:Controller.loadText
    	}));
    	//var container =$('<div><div class="followContainer" style="float:right"></div>'+ parsed.innerHTML + '<div>');
    	//div = followContent.appendTo(container('.followContainer'))
    	
    	
      
        output.appendTo(this.html);
        
    }
    
};


ClassData.prototype.loadMicrobloggingResponse = function(data) {
    for ( p in data ) {
        var author = '';
        for ( a in data[p].authorGroup ) {
            if ( author != '' ) {
                author = author + ',';
            }
            author = author + data[p].authorGroup[a].displayName;
        }
        var div = $('<div>')
            .addClass("microblogPost")
            .appendTo(this.html);
        $('<p>' + author + ':&nbsp;' + data[p].microblogText + '</p>')
            .appendTo(div);
        $('<p>' + Helper.timestampToDate(data[p].microblogTime) + ' (' + data[p].microblogID + ')</p>')
            .addClass("time")
            .appendTo(div);
    }
};

ClassData.prototype.setInfo = function(type,path) {
    this.info = {'type':type,'path':path};
};

ClassData.prototype.setType = function(type) {
    if ( typeof this.info != 'object' || this.info == undefined || this.info['type'] == undefined ) {
        this.info['type'] = type;
    }
};
