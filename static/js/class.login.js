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




ClassLogin.prototype.setLoginButtonState = function() {  
	Login.root = $('#login')
        .empty();
    if ( User.isLoggedIn() == true ) {
    	//Show Logout Link
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
    
    Login.formType = {'type':'register'};
    Login.formBuilder= new ClassFormBuilder();
    Login.formBuilder.open(Login.container ,'margin: auto; width: 200px;' );
    Login.formBuilder.createInputField('name','Name','','<input type="text">');
    Login.formBuilder.createInputField('email','E-Mail','','<input type="text">');
    Login.formBuilder.createInputField('password','Passwort','','<input type="password">');
    Login.formBuilder.createInputField('password2','Passwort wiederholen','','<input type="password">');
    Login.formBuilder.createButton('submit','Registrieren','margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel','Abbrechen','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
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
    
    Login.formType = {'type':'login'};
    Login.formBuilder= new ClassFormBuilder();
    Login.formBuilder.open(Login.container ,'margin: auto; width: 200px;' );
    Login.formBuilder.createInputField('name','Name','','<input type="text">',Login.checkKey);
    Login.formBuilder.createInputField('password','Passwort','','<input type="password">',Login.checkKey);
    Login.formBuilder.createButton('submit','Einloggen','margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel','Abbrechen','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
    Login.formBuilder.createButton('showRecovery','Passwort vergessen?','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.showRecoveryFormByName)

};
ClassLogin.prototype.showRecoveryFormByName = function() {
    Login.overlay = $('#overlay');
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    Login.formType = {'type':'recoverByName'};
    Login.formBuilder= new ClassFormBuilder();
    Login.formBuilder.open(Login.container ,'margin: auto; width: 200px;' );
    Login.formBuilder.createInputField('name','Benutzername','','<input type="text">',Login.checkKey);
    Login.formBuilder.createButton('submit','Wiederherstellung mit Benutzername','margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel','Abbrechen','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
    Login.formBuilder.createButton('showRecovery','Nutzername Vergessen?','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.showRecoveryFormByMail)
};
ClassLogin.prototype.showRecoveryFormByMail = function() {
    Login.overlay = $('#overlay');
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    Login.formType = {'type':'recoverByMail'};
    Login.formBuilder= new ClassFormBuilder();
    Login.formBuilder.open(Login.container ,'margin: auto; width: 200px;' );
    Login.formBuilder.createInputField('mail','Email','','<input type="text">',Login.checkKey);
    Login.formBuilder.createButton('submit','Wiederherstellung mit Emailadresse','margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel','Abbrechen','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
    Login.formBuilder.createButton('showRecovery','Doch per Name?','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.showRecoveryFormByName)
};

ClassLogin.prototype.submit = function() {
    switch ( Login.formType['type'] ) {
        case 'login': return Login.submitLogin();
        case 'register': return Login.submitRegister();
        case 'recoverByName': return Login.submitRecoveryByName();
        case 'recoverByMail': return Login.submitRecoveryByMail();
    }
    return false;
};

ClassLogin.prototype.submitLogin = function() {
    var tmp = {
        'username': Login.formBuilder.get('name'),
        'password': Login.formBuilder.get('password')
    };
    if ( tmp['name'] == '' 
        || tmp['password'] == '' ) {
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
    RqHandler.post({
        url: '.json_login',
        data: tmp,
        success: Login.handleRequest
    });
   
}

ClassLogin.prototype.submitRecoveryByMail = function() {
 	var tmp = {
       'emailAddress': Login.formBuilder.get('mail')
    };
    if ( tmp['emailAddress'] == '') 
 	{
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
    RqHandler.post({
        url: '.json_accountResetRequestByMail',
        data: tmp,
    });
 }
 
 
ClassLogin.prototype.submitRecoveryByName = function() {
 	var tmp = {
        'displayName': Login.formBuilder.get('name')
    };
    if ( tmp['displayName'] == '') 
 	{
        alert('Bitte fülle alle Felder aus!');
        return false;
    }
    RqHandler.post({
        url: '.json_accountResetRequestByName',
        data: tmp
    });
 } 
 

ClassLogin.prototype.submitRegister = function() {
 	var tmp = {
        'displayName': Login.formBuilder.get('name'),
        'emailAddress': Login.formBuilder.get('email'),
        'password': Login.formBuilder.get('password'),
        'password2': Login.formBuilder.get('password2')
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
       RqHandler.post({
        url: '.json_accountRegistration',
        data: tmp
    });
}
 
 
ClassLogin.prototype.submitActivation = function(activationKey) {
	var tmp = {
    	'activationKey': activationKey,
    };
	RqHandler.post({
        url: '.json_accountActivation',
        data: tmp
    	});
 	}	
 

ClassLogin.prototype.submitRecovery = function(activationKey) {
 	var tmp = {
        'activationKey': activationKey,
    };
 	RqHandler.post({
        url: '.json_accountResetConfirmation',
        data: tmp
    });
}