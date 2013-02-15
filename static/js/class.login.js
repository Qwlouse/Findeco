/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert <justus_wingert@web.de>                            *
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
 
function ClassLogin() {}
var Login = new ClassLogin();

ClassLogin.prototype.form = {};
ClassLogin.prototype.user = null;

ClassLogin.prototype.hasUser = function() {
    if ( Login.user != null ) {
        return true;
    }
    return false;
}

ClassLogin.prototype.fieldClickHandler = function() {
    $(this).attr('id','');
}

ClassLogin.prototype.show = function() {
    Login.root = $('#login');
    console.log('hello');
    if ( Login.hasUser() ) {
        console.log('bye');
        // Show Userinfo
        return;
    }
    console.log('here we go');
    // Show Login form.
    Login.form = {};
    Login.form['name'] = $('<span id="inputname"><input type="text"></span>')
        .keydown(Login.fieldClickHandler)
        .click(function() {this.firstChild.focus();})
        .appendTo(Login.root);
    Login.form['password'] = $('<span id="inputpass"><input type="password"></span>')
        .keydown(Login.fieldClickHandler)
        .click(function() {this.firstChild.focus();})
        .appendTo(Login.root);
    Login.form['submit'] = $('<div class="button">Einloggen</div>')
        .appendTo(Login.root);
};