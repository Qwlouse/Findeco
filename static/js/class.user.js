/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Maik Nauheim <mail@maik-nauheim.de>                            *
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
 
/**
 * Creates an instance of User.
 *
 * @constructor
 * @this {User}
 */
function ClassUser() {
	/** @private */ this.loggedIn = false;
}

/**
 * Returns the current loginstatus of user
 *
 * @return {Boolean} The Loginstatus of the user
 */
ClassUser.prototype.isLoggedIn= function(){
	/** TODO: We need to Drop isLoggedIn. This can be done either by getting Django Cookie or setting another one with the same properties**/
	return this.loggedIn;
}

/**
 * Handler for called on Logout
 *
 * @return {Boolean} success
 */
ClassUser.prototype.LogoutSuccess= function(){
	this.loggedIn = false;
	return true;
}


/**
 * Handler for called on Login
 *
 * @return {Boolean} success
 */
ClassUser.prototype.LoginSuccess= function(){
	this.loggedIn = true;
	return true;
}
 
 
 