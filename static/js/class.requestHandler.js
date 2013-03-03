/** ************************************************************************************
 * Copyright (c) 2013 Maik Nauheim findeco@maik-nauheim.de                        *
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





function ClassRequestHandler() {}
var RqHandler = new ClassRequestHandler();

ClassRequestHandler.prototype.post = function (e) {
		callback=e.success;
		e.type= 'POST';	
		e.dataType = 'json';
		e.beforeSend = function(xhr, settings) { xhr.setRequestHeader("X-CSRFToken", Helper.getCSRFToken()); }
		e.success = function(data) { RqHandler.callback(data, callback); }
		$.ajax(e);
	
}
ClassRequestHandler.prototype.get  = function (e) {
	return function(){ 
	callback=e.success;
	e.type= 'GET';	
	e.dataType = 'json';
	e.beforeSend = function(xhr, settings) { xhr.setRequestHeader("X-CSRFToken", Helper.getCSRFToken()); }
	e.success = function(data) { RqHandler.callback(data, callback); }
	$.ajax(e);
	}
}




ClassRequestHandler.prototype.callback = function (data,callback) {	
	
	if ( typeof data['errorResponse'] !=  'undefined') {
		var inserts=	data['errorResponse']['additionalInfo'];
		var text = Language.get(data['errorResponse']['errorID']); 
		alert(text.format(inserts));
		return false;  	    
        
    }
    if (callback == 'none'){
    	return false;
    }
    
    if (typeof callback != 'undefined'){ 
		callback(data);
	}else
	{
		for (var SuccessID in data) {
   			break;    // or do something with it and break
    	}
    	
		alert(Language.get(SuccessID +'Success'));
	
	}

}








