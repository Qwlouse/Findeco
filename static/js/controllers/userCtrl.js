/****************************************************************************************
 * Copyright (c) 2014 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
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

'use strict';

findecoApp.controller('FindecoUserCtrl', function ($scope, $rootScope, Navigator, Message, User, Fesettings ) {
    $scope.user = User;
    $scope.fesettings = Fesettings;

    // used for login and registration
    $scope.username = "";
    $scope.password = "";
    $scope.password2 = "";
    $scope.mail = "";
    $scope.TOS = false;
    $scope.DPR = false;
    $scope.attemptedRegister = false;
    $scope.allFieldsFilledCorrectly = false;
    $scope.serverError = false;

    // used for profile
    $scope.emailChanged = false;
    $scope.usernameChanged = false;
    $scope.passwordChanged = false;

    $scope.changeEmailError = false;
    $scope.changeUsernameError = false;
    $scope.changePasswordError = false;


    $scope.force_get_username_password = function() {
        // HACK to make autofill of browsers work.
        // This is because browser autofill does not trigger an event, so
        // Angular does not know about the changes.
        // therefore we check ourselves to make sure we've got the latest values
        $scope.username = document.getElementById('usernameInput').value;
        $scope.password = document.getElementById('passwordInput').value;
    };

    $scope.login = function () {
        $scope.force_get_username_password();
        User.login($scope.username, $scope.password).success(function () {
            Navigator.changePath('/');
        });
    };

    $scope.register = function () {
        $scope.attemptedRegister = true;
        $scope.serverError = false;
        $scope.allFieldsFilledCorrectly =
            ($scope.password != '') &&
            ($scope.mail != '') &&
            ($scope.username != '') &&
            ($scope.password == $scope.password2) &&
            ($scope.TOS == true) &&
            ($scope.DPR == true);

        if ($scope.allFieldsFilledCorrectly) {
            User.register($scope.username, $scope.password, $scope.mail).success(function () {
                Navigator.changePath('/registerSuccess');
            }).error(function(d, e, f) {
                $scope.serverError = d.errorResponse;
                $scope.allFieldsFilledCorrectly = false;
            });
        }
    };

    $scope.storeUserDescription = function () {
        $scope.storeUserSettings().success(function() {
            $scope.profileDescription.$setPristine();
        });
    };


    $scope.storeUserEMail = function () {
        $scope.storeUserSettings().success(function() {
            $scope.emailChanged = true;
            $scope.changeEmailError = false;
            $scope.profileEMail.$setPristine();
        }).error(function (d) {
            $scope.changeEmailError = d.errorResponse;
        });
    };

    $scope.storeUserName = function() {
        var r = window.confirm("Dein Benutzername wird im gesamten System geändert. Das kann deine Follower verwirren. Außerdem kann es eine Weile dauern bis die Änderung überall wirksam ist.\n Sicher dass du deinen Namen ändern möchtest?");
        if (!r) { return; }

        User.displayName = User.newDisplayName;
        $scope.storeUserSettings().success(function() {
            $scope.usernameChanged = true;
            $scope.changeUsernameError = false;
            $scope.profileUsername.$setPristine();
        }).error(function(d) {
            $scope.changeUsernameError = d.errorResponse;
        });
    };

    $scope.storeUserSettings = function () {
        return User.storeSettings().error(function () {
            User.loadSettings();
        });
    };

    $scope.changePassword = function () {
        if ($scope.password == $scope.password2) {
            User.changePassword($scope.password).success(function () {
                $scope.passwordChanged = true;
                $scope.changePasswordError = false;
                $scope.password = "";
                $scope.password2 = "";
                $scope.profilePassword.$setPristine();
            }).error(function(d) {
                $scope.changePasswordError = d.errorResponse;
            });
        } else {
            $scope.changePasswordError = {
                errorID: "_passwordsDidNotMatch_",
                additionalInfo: {}};
        }
    };

    $scope.deleteAccount = function () {
        if (confirm(Message.localize('_deleteAccountQuestion_'))) {
            User.deleteAccount().success(function () {
                User.logout();
                Navigator.changePath('/');
            });
        }
    };

    $scope.recoverByMail = function () {
        User.recoverByMail($scope.mail).success(function () {
            Navigator.changePath('/');
            Message.send("success", "_accountRecoveryFinished_");
        });
    };

    $scope.recoverByUsername = function () {
        User.recoverByUsername($scope.username).success(function () {
            Navigator.changePath('/');
            Message.send("success", "_accountRecoveryFinished_");
        });
    };

    $scope.$on('$locationChangeStart', function(event) {
        if (!event.defaultPrevented && $scope.user.hasUnsavedChanges()) {
            var r = window.confirm("Du hast Dinge geändert, aber noch nicht gespeichert\n Wenn du die Seite verlässt gehen dese verloren.\n Verlassen?");
            if (r) {
                $scope.user.resetChanges();
            } else {
                event.preventDefault();
            }
        }
    });
});
