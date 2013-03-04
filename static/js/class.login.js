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
 
 
 // TODO: Error Handling
function ClassLogin() {}



ClassLogin.prototype.form = {}; 
ClassLogin.prototype.rqhandler= RqHandler;

ClassLogin.prototype.checkKey = function (e) {
    if ( e.which == 13 ) {
        Login.submit();
    }
}

ClassLogin.prototype.close = function () {
    if ( $(this).attr('id') == 'overlay' || $(this).attr('id') == 'cancelbutton' ) {
        $('#overlay').hide();
    }
}

ClassLogin.prototype.handleRequest = function(data) {

    if ( typeof data['loginResponse'] !=  'undefined') {
    	
	    User.LoginSuccess();
	    Login.setLoginButtonState();
	    Login.overlay
	        .hide()
	        .empty();
    }
    
        
}

ClassLogin.prototype.logout = function() {
    $.get('.json_logout',function(data) {
        User.LogoutSuccess();
        Login.setLoginButtonState();
        alert(data['logoutResponse']['farewellMessage']);
    },'json');
}

ClassLogin.prototype.fieldClickHandler = function() {
    $(this).attr('id','');
}


ClassLogin.prototype.createTableFormField = function(name,input,targetTable,func) {
    var tr = $('<tr>')
        .appendTo(targetTable);
    $('<td>' + name + '</td>')
        .appendTo(tr);
    return $(input)
        .keypress(func)
        .appendTo(
            $('<td>')
                .appendTo(tr)
            );
    
}

ClassLogin.prototype.setLoginButtonState = function() { 
	 Login.root = $('#login')
        .empty();
    if ( User.isLoggedIn() == true ) {
        $('<div class="button">Ausloggen</div>')
            .attr('style','margin-bottom: 10px;')
            .click(Login.logout)
            .appendTo(Login.root);
        
    }else{
    // Show Login link.
    $('<div class="button">Einloggen</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.showLoginForm)
        .appendTo(Login.root);
    $('<div class="button">Registrieren</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.showRegisterForm)
        .appendTo(Login.root);
    }
}

ClassLogin.prototype.showRegisterForm = function() {
    Login.overlay = $('#overlay')
        .click(Login.close)
        .show();
    Login.overlay.empty();
    
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    
    var table = $('<table>')
        .attr('style','margin: auto; width: 200px;')
        .appendTo(Login.container);
    
    Login.form = {'type':'register'};
    Login.form['name'] = Login.createTableFormField('Name','<input type="text">',table);
    Login.form['email'] = Login.createTableFormField('E-Mail','<input type="text">',table);
    Login.form['password'] = Login.createTableFormField('Passwort','<input type="password">',table);
    Login.form['password2'] = Login.createTableFormField('Passwort wiederholen','<input type="password">',table);
    tr = $('<tr>')
        .appendTo(table);
    td = $('<td colspan="2">')
        .appendTo(tr);
    Login.form['submit'] = $('<div id="inputsubmit" class="button">Registrieren</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.submit)
        .appendTo(td);
    Login.form['cancel'] = $('<div id="cancelbutton" class="button">Abbrechen</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.close)
        .appendTo(td);
   
}

ClassLogin.prototype.showLoginForm = function() {
    Login.overlay = $('#overlay')
        .click(Login.close)
        .show();
    Login.overlay.empty();
    
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    
    var table = $('<table>')
        .attr('style','margin: auto; width: 200px;')
        .appendTo(Login.container);
    
    Login.form = {'type':'login'};
    Login.form['name'] = Login.createTableFormField('Name','<input type="text">',table,Login.checkKey);
    Login.form['password'] = Login.createTableFormField('Passwort','<input type="password">',table,Login.checkKey);
    tr = $('<tr>')
        .appendTo(table);
    td = $('<td colspan="2">')
        .appendTo(tr);
    Login.form['submit'] = $('<div id="inputsubmit" class="button">Einloggen</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.submit)
        .appendTo(td);
    Login.form['cancel'] = $('<div id="cancelbutton" class="button">Abbrechen</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.close)
        .appendTo(td);
     $('<br><div class="button">Passwort vergessen? </div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.showRecoveryFormByName)
        .appendTo(td);
};
ClassLogin.prototype.showRecoveryFormByName = function() {
    Login.overlay = $('#overlay');
    
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    
    var table = $('<table>')
        .attr('style','margin: auto; width: 200px;')
        .appendTo(Login.container);
        
    Login.form = {'type':'recoverByName'};
    Login.form['name'] = Login.createTableFormField('Benutzername:','<input type="text">',table,Login.checkKey);
    tr = $('<tr>')
        .appendTo(table);
    td = $('<td colspan="2">')
        .appendTo(tr);
    Login.form['submit'] = $('<div id="inputsubmit" class="button">Wiederherstellung mit Benutzername</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.submit)
        .appendTo(td);
    Login.form['cancel'] = $('<div id="cancelbutton" class="button">Abbrechen</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.close)
        .appendTo(td);
    $('<br><div class="button">Nutzername Vergessen?</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.showRecoveryFormByMail)
        .appendTo(td);

};
ClassLogin.prototype.showRecoveryFormByMail = function() {
    Login.overlay = $('#overlay');
    
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    
    var table = $('<table>')
        .attr('style','margin: auto; width: 200px;')
        .appendTo(Login.container);
    Login.form = {'type':'recoverByMail'};
    Login.form['mail'] = Login.createTableFormField('Email:','<input type="text">',table,Login.checkKey);
    tr = $('<tr>')
        .appendTo(table);
    td = $('<td colspan="2">')
        .appendTo(tr);
    Login.form['submit'] = $('<div id="inputsubmit" class="button">Wiederherstellung mit Emailadresse</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.submit)
        .appendTo(td);
    Login.form['cancel'] = $('<div id="cancelbutton" class="button">Abbrechen</div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.close)
        .appendTo(td);
    $('<br><div class="button">Doch per Name? </div>')
        .attr('style','margin-bottom: 10px;')
        .click(Login.showRecoveryFormByName)
        .appendTo(td);

};

ClassLogin.prototype.submit = function() {
    switch ( Login.form['type'] ) {
        case 'login': return Login.submitLogin();
        case 'register': return Login.submitRegister();
        case 'recoverByName': return Login.submitRecoveryByName();
        case 'recoverByMail': return Login.submitRecoveryByMail();
    }
    return false;
};

ClassLogin.prototype.submitLogin = function() {
    var tmp = {
        'username': Login.form['name'].val(),
        'password': Login.form['password'].val()
    };
    if ( tmp['name'] == '' 
        || tmp['password'] == '' ) {
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
    Login.rqhandler.post({
        url: '.json_login',
        data: tmp,
        success: Login.handleRequest
    });
   
}

ClassLogin.prototype.submitRecoveryByMail = function() {
 	var tmp = {
       'emailAddress': Login.form['mail'].val()
    };
    if ( tmp['emailAddress'] == '') 
 	{
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
    Login.rqhandler.post({
        url: '.json_accountResetRequestByMail',
        data: tmp,
    });
 }
 
 
ClassLogin.prototype.submitRecoveryByName = function() {
 	var tmp = {
        'displayName': Login.form['name'].val()
    };
    if ( tmp['displayName'] == '') 
 	{
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
    Login.rqhandler.post({
        url: '.json_accountResetRequestByName',
        data: tmp
    });
 } 
 

ClassLogin.prototype.submitRegister = function() {
 	var tmp = {
        'displayName': Login.form['name'].val(),
        'emailAddress': Login.form['email'].val(),
        'password': Login.form['password'].val(),
        'password2': Login.form['password2'].val()
    };
    if ( tmp['displayName'] == '' 
    	|| tmp['emailAddress'] == ''
        || tmp['password'] == ''
        || tmp['password2'] == '' ) {
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
       if ( tmp['password'] != tmp['password2'] ) {
        alert('Die Passwörter stimmen nicht überein');
        return false;
    }
    Login.rqhandler.post({
        url: '.json_accountRegistration',
        data: tmp
    });
}
 
 
ClassLogin.prototype.submitActivation = function(activationKey) {
	var tmp = {
    	'activationKey': activationKey,
    };
   	Login.rqhandler.post({
        url: '.json_accountActivation',
        data: tmp
    	});
 	}	
 

ClassLogin.prototype.submitRecovery = function(activationKey) {
 	var tmp = {
        'activationKey': activationKey,
    };
   	Login.rqhandler.post({
        url: '.json_accountResetConfirmation',
        data: tmp
    });
}