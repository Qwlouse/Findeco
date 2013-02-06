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

var boxCount = 0;

function ClassBox() { this.id = ++boxCount; this.element = $('<div id="box' + this.id + '"></div>'); };

ClassBox.prototype.addButtons = function() {
    var arguments = this.element.children('div.arguments');
    var text = this.element.children('div.text');
    var buttons = this.element.children('div.buttons');
    
    $('<div style="margin-bottom: 10px;">Zeige Argumente</div>')
        .addClass('button')
        .click(function () {
            Controller.loadArguments();
        })
        .appendTo(arguments);
    $('<div style="margin-bottom: 10px;">Zeige Text</div>')
        .addClass('button')
        .click(function () {
            Controller.loadText();
        })
        .appendTo(text);
    
    $('<div style="margin-bottom: 10px;">Abschnitt hinzuf&uuml;gen</div>')
        .addClass('button')
        .addClass('smallbutton')
        .click(function () {
            
        })
        .appendTo(buttons);
    
    $('<div style="margin-bottom: 10px;">Argument hinzuf&uuml;gen</div>')
        .addClass('button')
        .addClass('smallbutton')
        .click(function () {
            
        })
        .appendTo(buttons);
    
    
}

ClassBox.prototype.printData = function(data) {
    var target = this.element;
    switch ( data.getType() ) {
        case 'index':
            target = this.element.children('div.indizes');
        break;
        case 'text':
            target = this.element.children('div.text');
        break;
        case 'argument':
            target = this.element.children('div.arguments');
        break;
        case 'graphdata':
            target = this.element.children('div.graphdata');
        break;
    }
    
    if ( this.element.parent().hasClass('left') ) {
        var target = this.element;
    }
    target.empty();
    
    data.getJQueryObject().appendTo(target);
}

ClassBox.prototype.empty = function() {
    if ( this.type == 'center' ) {
        this.element.children().empty();
        this.addButtons();
    } else {
        this.element.empty();
    }
}

ClassBox.prototype.show = function(position,container) {
    this.type = position;
    if ( container != null ) {
        this.element.appendTo(container.element)
    } else {
        this.element.appendTo($('#container'));
        this.element.addClass('box');
    }
    
    if ( position != null ) {
        this.element.addClass(position);
    }
    
    if ( position == 'center' ) {
        $('<div>')
            .addClass('graphdata')
            .appendTo(this.element);
        $('<div>')
            .addClass('indizes')
            .appendTo(this.element);
        $('<div>')
            .addClass('arguments')
            .appendTo(this.element);
        $('<div>')
            .addClass('text')
            .appendTo(this.element);
        $('<div>')
            .addClass('buttons')
            .appendTo(this.element);
        
        this.addButtons();
        
        // console.log(this.element,this.element.children());
    } else if ( position == 'swap' ) {
        $('<p>' + this.id + '</p>').appendTo(this.element);
        this.blind = $('<div id="boxswap' + this.id + '" class="blind">');
        this.blind.appendTo(container.element);
        this.blind.click(this.swap);
        this.element.click(this.swap);
        
        this.element.hide();
    }
}

ClassBox.prototype.swap = function(element) {
    var id = Helper.getId(element.target.id);
    
    if ( id == null ) {
        return;
    }
    
    var boxIsTarget = false;
    if ( element.target.id == 'box' + id ) {
        var boxIsTarget = true;
    }
    
    if ( boxIsTarget ) {
        BoxRegister.get(id).blind.show();
        BoxRegister.get(id).element.hide();
    } else {
        BoxRegister.hideAll();
        BoxRegister.get(id).blind.hide();
        BoxRegister.get(id).element.show();
        var newStyle = 'width: ' + ( $(window).width() / 4 ) + 'px;';
        BoxRegister.get(id).element.attr('style',newStyle);
    }
}
