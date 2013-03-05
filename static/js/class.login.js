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
 
 /**
 * Handles the login/logout logic as well as tee representation in the frontend
 *
 * @constructor
 * @this {Login}
 */
function ClassLogin() {}

/**
 * Handler for onKey event. Autosubmits form
 * @todo Does this really work?
 */
ClassLogin.prototype.checkKey = function (e) {
    if ( e.which == 13 ) {
        Login.submit();
    }
}

/**
 * Hides login Overlay
 * @todo Should eventually be in Controller
 */
ClassLogin.prototype.close = function () {
    if ( $(this).attr('id') == 'overlay' || $(this).attr('id') == 'cancelbutton' ) {
        $('#overlay').hide();
    }
}

/**
 * Handles successfull requests 
 */
ClassLogin.prototype.handleRequest = function(data) {
    if ( typeof data['loginResponse'] !=  'undefined') {
    	User.LoginSuccess();
	    Login.setLoginButtonState();
	    Login.overlay
	        .hide()
	        .empty();
    }
}

/**
 * Handles a clicked Logout Button
 */
ClassLogin.prototype.logout = function() {
    $.get('.json_logout',function(data) {
        User.LogoutSuccess();
        Login.setLoginButtonState();
        alert(data['logoutResponse']['farewellMessage']);
    },'json');
}

/**
 * Maybe Not in Use
 * @todo Check if it is in Use
 */
ClassLogin.prototype.fieldClickHandler = function() {
    $(this).attr('id','');
}

/**
 * Sets the state of login buttons corresponding to the user User.isLoggedIn()
 */
ClassLogin.prototype.setLoginButtonState = function() {  
	Login.root = $('#login')
        .empty();
    if ( User.isLoggedIn() == true ) {
    	//Show Logout Link
        $('<div class="button">'+Language.get('doLogout')+'</div>')
            .attr('style','margin-bottom: 10px;')
            .click(Login.logout)
            .appendTo(Login.root);
        
    }else{
    	// Show Login link.
    	$('<div class="button">'+Language.get('doLogin')+'</div>')
        	.attr('style','margin-bottom: 10px;')
        	.click(Login.showLoginForm)
        	.appendTo(Login.root);
    	$('<div class="button">'+Language.get('doRegistration')+'</div>')
        	.attr('style','margin-bottom: 10px;')
        	.click(Login.showRegisterForm)
        	.appendTo(Login.root);
    }
}

/**
 * Shows form for registration process
 */
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
    Login.formBuilder.createInputField('name',Language.get('username'),'','<input type="text">');
    Login.formBuilder.createInputField('email',Language.get('email'),'','<input type="text">');
    Login.formBuilder.createInputField('password',Language.get('password'),'','<input type="password">');
    Login.formBuilder.createInputField('password2',Language.get('passwordAgain'),'','<input type="password">');
    Login.formBuilder.createButton('submit',Language.get('submit'),'margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel',Language.get('cancel'),'margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
}

/**
 * Shows form for login process
 */
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
    Login.formBuilder.createInputField('name',Language.get('username'),'','<input type="text">',Login.checkKey);
    Login.formBuilder.createInputField('password',Language.get('password'),'','<input type="password">',Login.checkKey);
    Login.formBuilder.createButton('submit',Language.get('doLogin'),'margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel',Language.get('cancel'),'margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
    Login.formBuilder.createButton('showRecovery',Language.get('qForgotPassword'),'margin-bottom: 10px;','id="cancelbutton" class="button"',Login.showRecoveryFormByName)

};

/**
 * Show form for password recovery by name process
 */
ClassLogin.prototype.showRecoveryFormByName = function() {
    Login.overlay = $('#overlay');
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    Login.formType = {'type':'recoverByName'};
    Login.formBuilder= new ClassFormBuilder();
    Login.formBuilder.open(Login.container ,'margin: auto; width: 200px;' );
    Login.formBuilder.createInputField('name',Language.get('username'),'','<input type="text">',Login.checkKey);
    Login.formBuilder.createButton('submit',Language.get('recovertWUsername'),'margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel',Language.get('cancel'),'margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
    Login.formBuilder.createButton('showRecovery',Language.get('qForgotUserName'),'margin-bottom: 10px;','id="cancelbutton" class="button"',Login.showRecoveryFormByMail)
};

/**
 * Show form for password recovery by email process
 */
ClassLogin.prototype.showRecoveryFormByMail = function() {
    Login.overlay = $('#overlay');
    Login.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Login.overlay);
    Login.formType = {'type':'recoverByMail'};
    Login.formBuilder= new ClassFormBuilder();
    Login.formBuilder.open(Login.container ,'margin: auto; width: 200px;' );
    Login.formBuilder.createInputField('mail',Language.get('email'),'','<input type="text">',Login.checkKey);
    Login.formBuilder.createButton('submit',Language.get('recovertWEmail'),'margin-bottom: 10px;','id="inputsubmit" class="button"',Login.submit)
    Login.formBuilder.createButton('cancel','Abbrechen','margin-bottom: 10px;','id="cancelbutton" class="button"',Login.close)
    Login.formBuilder.createButton('showRecovery',Language.get('qForgotPassword'),'margin-bottom: 10px;','id="cancelbutton" class="button"',Login.showRecoveryFormByName)
};

/**
 * Submithandler for all submitted forms. Data is transmitted to the specific handlers selected by Login.formType
 */
ClassLogin.prototype.submit = function() {
    switch ( Login.formType['type'] ) {
        case 'login': return Login.submitLogin();
        case 'register': return Login.submitRegister();
        case 'recoverByName': return Login.submitRecoveryByName();
        case 'recoverByMail': return Login.submitRecoveryByMail();
    }
    return false;
};

/**
 * Submithandler for all submitted login forms
 */
ClassLogin.prototype.submitLogin = function() {
    var tmp = {
        'username': Login.formBuilder.get('name'),
        'password': Login.formBuilder.get('password')
    };
    if ( tmp['name'] == '' 
        || tmp['password'] == '' ) {
        alert(Language.get('formMissingField'));
        return false;
    }
    RqHandler.post({
        url: '.json_login',
        data: tmp,
        success: Login.handleRequest
    });
   
}

/**
 * Submithandler for all submitted recovery by email forms
 */
ClassLogin.prototype.submitRecoveryByMail = function() {
 	var tmp = {
       'emailAddress': Login.formBuilder.get('mail')
    };
    if ( tmp['emailAddress'] == '') 
 	{
        alert(Language.get('formMissingField'));
        return false;
    }
    RqHandler.post({
        url: '.json_accountResetRequestByMail',
        data: tmp,
    });
 }
 
 /**
 * Submithandler for all submitted recovery by name forms
 */
ClassLogin.prototype.submitRecoveryByName = function() {
 	var tmp = {
        'displayName': Login.formBuilder.get('name')
    };
    if ( tmp['displayName'] == '') 
 	{
        alert(Language.get('formMissingField'));
        return false;
    }
    RqHandler.post({
        url: '.json_accountResetRequestByName',
        data: tmp
    });
 } 
 
 /**
 * Submithandler for all submitted recovery by name forms
 */
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
        alert(Language.get('formMissingField'));
        return false;
    }
       if ( tmp['password'] != tmp['password2'] ) {
        alert(Language.get('passwordMatch'));
        return false;
    }
       RqHandler.post({
        url: '.json_accountRegistration',
        data: tmp
    });
}
 
/**
 * Submits the given activation key to the server
 * @param {integer} activationKey Activation key to start password recovery
 */
ClassLogin.prototype.submitActivation = function(activationKey) {
	var tmp = {
    	'activationKey': activationKey,
    };
	RqHandler.post({
        url: '.json_accountActivation',
        data: tmp
    	});
 	}	
 
/**
 * Submits the given activation key to the server to start password recovery
 * @param {integer} activationKey Activation key to start password recovery
 */
ClassLogin.prototype.submitRecovery = function(activationKey) {
 	var tmp = {
        'activationKey': activationKey,
    };
 	RqHandler.post({
        url: '.json_accountResetConfirmation',
        data: tmp
    });
}