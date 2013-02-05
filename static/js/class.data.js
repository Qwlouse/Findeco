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

function ClassData(json) {this.load(json);}

ClassData.prototype.load = function(data) {
    this.json = data;
    
    this.html = $('<div>');
    this.html.addClass('innerContent');
    
    // console.log(data);
    
    for ( d in data ) {
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
    
    for ( d in data ) {
        // console.log(data[d]);
        $('<li>' + data[d].fullTitle + '</li>').appendTo(arguments[data[d].shortTitle]);
    }
}

ClassData.prototype.loadGraphDataResponse = function(data) {
    this.type = 'graphdata';
}

ClassData.prototype.loadIndexResponse = function(data) {
    this.type = 'index';
    
    parent = '';
    if ( typeof this.info == 'object' && this.info.path != undefined ) {
        parent = 'data-parent="' + this.info.path + '"';
    }
    
    for ( d in data ) {
        switch ( data[d].shortTitle ) {
            case 'pro': case 'neut': case 'con': this.loadArgumentResponse(data); return;
            default:
                if ( parent != '' ) {
                    var parentpath = this.info.path;
                    if ( parentpath.substring(parentpath.length-1) != '/' ) {
                        parentpath += '/';
                    }
                    DataRegister.setTitle(parentpath + data[d].shortTitle + '.' + data[d].index,data[d].fullTitle);
                }
                $('<h2 data-shortTitle="' + data[d].shortTitle + '" data-index="' + data[d].index + '"' + parent + '>' + data[d].fullTitle + '</h2>')
                    .appendTo(this.html)
                    .click(function () {
                        if ( $(this).attr('data-parent') == undefined ) {
                            Controller.loadIndexRelative($(this).attr('data-shortTitle') + '.' + $(this).attr('data-index'));
                        } else {
                            var parent = $(this).attr('data-parent');
                            if ( parent.substring(parent.length-1) != '/' ) {
                                parent += '/';
                            }
                            Controller.loadIndex(parent + $(this).attr('data-shortTitle') + '.' + $(this).attr('data-index'));
                        }
                    });
        }
    }
};

ClassData.prototype.loadTextResponse = function(data) {
    this.type = 'text';
    
    for ( p in data['paragraphs'] ) {
        $('<p>' + data['paragraphs'][p].wikiText + '</p>').appendTo(this.html);
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

ClassData.prototype.getJQueryObject = function() {
    return this.html;
}

ClassData.prototype.getType = function() {
    return this.type;
}

ClassData.prototype.setInfo = function(type,path) {
    this.info = {'type':type,'path':path};
}

ClassData.prototype.getInfo = function() {
    return this.info;
}
