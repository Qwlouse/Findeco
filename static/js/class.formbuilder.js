/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2013           Mail Nauheim <findeco@maik-nauheim.de>					* 
 *                    					derived from work of							*
 *                    			Justus Wingert <justus_wingert@web.de>                  *                                       *
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


/**
 * Provides an Interface for generating simple Forms.
 *
 * @constructor
 * @this {FormBuilderObject}
 */
function ClassFormBuilder() {
	this.fieldArray = new Array();
};
/**
 * Returns the current loginstatus of user
 *
 * @return {Boolean} The Loginstatus of the user
 */
ClassFormBuilder.prototype.open = function(append, style) {
	 this.table = $('<table>')
     	.attr('style',style)
     	.appendTo(append);
}
/**
 * Creates a Input Field on the Bottom of a Form
 *
 * @param {String} id A Human readable reference to the field
 * @param {String} description The description viewed in the Form
 * @param {String} style A String with CSS Attributes to be added to the Button
 * @param {String} input an HTML input tag (This will be gone in the next cleanup)
 * @param {String} event connection to the onClick event  
 */
ClassFormBuilder.prototype.createInputField = function(id,name,style,input,event) {
    var tr = $('<tr>')
        .appendTo(this.table);
    $('<td>' + name + '</td>')
        .appendTo(tr);
    this.fieldArray[id] =  $(input)
        .keypress(event)
        .appendTo(
            $('<td>')
                .appendTo(tr)
            );
}
/**
 * Creates a Button on the Bottom of a Form
 *
 * @param {String} id A Human readable reference to the field
 * @param {String} description The description viewed in the Form
 * @param {String} style A String with CSS Attributes to be added to the Button
 * @param {String} divData A String for injection into the Div (i.e. 'id="eew" style="color:red"')
 * @param {String} event connection to the onClick event  
 */
ClassFormBuilder.prototype.createButton = function(id,description,style,divData,event) {
	var tr = $('<tr>')
		.appendTo(this.table);
	var td = $('<td colspan="2">')
     	.appendTo(tr);
 	$('<div '+divData+'>'+description+'</div>')
 		.attr('style',style)
 		.click(event)
 		.appendTo(td);
};
/**
 * Returns the Value of a Field stored by the Form Object.
 *
 * @param {String} id A Human readable reference to the field
 * @return {String} Value of requested form Field
 */
ClassFormBuilder.prototype.get = function(id) {
	return this.fieldArray[id].val()
}



