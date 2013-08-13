/****************************************************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim, Johannes Merkert       *
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

 /* Important: de_DE is the default language, add there under all circumstances! */
function ClassLanguage() {}

var Language = new ClassLanguage();

ClassLanguage.prototype.get = function (target) {
    switch (Settings.locales) {
        case 'de_DE':
            switch (target) {
                case 'lang_alertLoggedout':
                    return 'Du bist nicht mehr eingeloggt. Bitte lade die Seite neu.';
                case 'lang_follow0':
                    return 'Sie folgen dem Vorschlag nicht. Klicken sie zum folgen.';
                case 'lang_follow1':
                    return 'Sie folgen dem Vorschlag transitiv. Klicken sie zum entfolgen.';
                case 'lang_follow2':
                    return 'Sie folgen dem Vorschlag. Klicken sie zum entfolgen.';
                case 'lang_spam0':
                    return 'Diesen Vorschlag als Spam markieren.';
                case 'lang_spam1':
                    return 'Spammarkierung entfernen.';
                case 'UnknownEmailAddress':
                	return 'Die Emailaddresse \'{0}\' ist dem System nicht bekannt';
                case 'UnknownUser':
                	return 'Der User \'{0}\' ist dem System nicht bekannt';
                case 'UnknownNode':
                	return 'Der Pfad \'{0}\' ist dem System nicht bekannt';
                case 'MissingPOSTParameter':
                	return 'Der Post Parameter \'{0}\' fehlt';
                case 'IllegalPath':
                	return 'Der Pfad Parameter \'{0}\' ist ungültig'; 
                case 'NotAuthenticated':
                	return 'Sie sind nich angemeldet';     
      			case 'PermissionDenied':
                	return 'Zugriff verweigert'; 
				case 'DisabledAccount':
                	return 'Der Account \'{0}\' ist deaktiviert';
                case 'UsernameNotAvailable':
                	return 'Der Benutzername \'{0}\' ist nicht verfügbar';  
 				case 'EmailAddressNotAvailiable':
                	return 'Die Emailadresse \'{0}\' ist nicht verfügbar'; 
                case 'InvalidLogin':
                	return 'Die Loggindaten sind leider ungültig';
                case 'InvalidEmailAddress':
                	return 'Die Emailadresse \'{0}\' ist ungültig';
                case 'InvalidActivationKey':
                	return 'Der Aktivierungscode ist ungültig oder bereits verwendet';	
                case 'InvalidURL':
                	return 'Diese URL ist ungültig';
				//Common form errors
				case 'formMissingField':
                	return 'Bitte fülle alle Felder aus!';
				//Common single Words
				case 'doLogout':
                	return 'Ausloggen';
				case 'doLogin':
                	return 'Einloggen';
				case 'doRegistration':
                	return 'Registrieren';
                case 'username':
                	return 'Benutzername';
                case 'email':
                	return 'E-Mail';
				case 'password':
                	return 'Passwort';
				case 'passwordAgain':
                	return 'Passwort wiederholen';
				case 'submit':
                	return 'Absenden';
				case 'cancel':
                	return 'Abbrechen';
				//Login Forms and Registration
				case 'qForgotPassword':
                	return 'Passwort vergessen?';
				case 'qForgotUserName':
                	return 'Passwort vergessen?';
				case 'recoverWUsername':
                	return 'Wiederherstellung mit Username';
                case 'recoverWEmail':
                	return 'Wiederherstellung mit E-Mail';
				case 'passwordMatch':
					return 'Die Passwörter stimmen nicht überein';
                // Contribute.js
				case 'cont_leaveForm':
					return 'Wollen sie wirklich das Formular verlassen? Nicht gespeicherte Zwischenstände gehen so verloren.';
				case 'cont_textOptions':
                    return 'Textoptionen';
				case 'cont_arguments':
                    return 'Argumente';
				case 'cont_proArgument':
                    return 'Pro Argument';
				case 'cont_conArgument':
                    return 'Contra Argument';
				case 'cont_neutArgument':
                    return 'Neutrales Argument';
				case 'cont_newNode':
                    return 'Neuer Abschnitt';
				case 'cont_newAlternative':
                    return 'Neue Alternative';
				case 'cont_newDerivate':
                    return 'Neue Weiterentwicklung';
				case 'cont_titleEditor':
				    return 'wikiText-Editor';
				case 'cont_derivateDesc':
				    return 'Neue Weiterentwicklung (Beschreibung)';
				// automatically called messages
                case 'accountRegistrationResponseSuccess':
                	return 'Die Registrierung war erfolgreich!! \n Du erhälst in den nächsten Minuten eine Aktivierungsemail.';
                case 'accountActivationResponseSuccess':
                	return 'Dein Account wurde gerade freigeschaltet. Du kannst dich jetzt einloggen';
                case 'accountResetRequestByNameResponseSuccess':
                	return 'Wir haben dir eine Wiederherstellungsmail an deine Emailadresse gesendet.';
                case 'accountResetRequestByMailResponseSuccess':
                	return 'Wir haben dir eine Wiederherstellungsmail an deine Emailadresse gesendet.';
                case 'accountResetConfirmationResponseSuccess':
                	return 'Die Wiederherstellung war erfolgreich. Wir haben dir ein neues Passwort zugesendet.';
                
                	
                // handling for Serverside faults
                case 'httpUnhandledResponse':
                    return 'Ein unbehandelter HTTP fehler ist aufgetreten.' ;
                case 'httpProposalNotFound':
                    return 'Diese URL ist ungültig oder der Vorschlag existiert nicht.';
                case 'httpInternalServerError':
                    return 'Ein Serverfehler ist aufgetreten. Bitte laden sie die Seite erneut';
                
                
                default:
                    return 'Es wurde keine Übersetzung für ' + target + ' definiert. ';
                
               
            }
            break;
        case 'en_GB':
            switch (lang) {
                default:
                    return 'undefined';
            }
            break;
    }
};