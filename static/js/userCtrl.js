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

'use strict';

function FindecoUserCtrl($scope, User, $rootScope, $routeParams, Message, Navigator) {
    $scope.user = User;
    $scope.displayNameTmp = User.displayName;
    $scope.followUser = User.markUser;

    // used for login and registration
    $scope.username = "";
    $scope.password = "";
    $scope.password2 = "";
    $scope.mail = "";
    $scope.TOS = false;
    $scope.DPR = false;

    $scope.login = function () {
        User.login($scope.username, $scope.password).success(function () {
            Navigator.changePath('/');
        });
    };

    $scope.logout = function () {
        User.logout().success(function () {
            Navigator.changePath('/');
        });
    };

    $scope.register = function () {
        var fields_filled_correctly = true;
        if (($scope.password == '') || ($scope.mail == '') || ($scope.username == '')) {
            Message.send("error", "_accountFieldsMissing_");
            fields_filled_correctly = false;
        }
        if ($scope.password != $scope.password2) {
            Message.send("error", "_accountPasswordsNotMatching_");
            fields_filled_correctly = false;
        }

        if ($scope.TOS != true) {
            Message.send("error", "_accountTosNotChecked_");
            fields_filled_correctly = false;
        }
        if ($scope.DPR != true) {
            Message.send("error", "_accountDprNotChecked_");
            fields_filled_correctly = false;
        }
        if (fields_filled_correctly) {
            User.register($scope.username, $scope.password, $scope.mail).success(function () {
                Navigator.changePath('/');
                Message.send("success", "_accountCheckEmails_");
            });
        }
    };

    $scope.storeUserSettings = function () {
        $scope.user.displayName = $scope.displayNameTmp;
        User.storeSettings().error(User.loadSettings).success(function () {
            Message.send("success", "_settingsChanged_");
        });
    };

    $scope.changePassword = function () {
        if ($scope.password == $scope.password2) {
            User.changePassword($scope.password).success(function () {
                Message.send("success", "_passwordChanged_");
                $scope.password = "";
                $scope.password2 = ""
            });
        } else {
            Message.send("error", "_passwordsDidNotMatch_");
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
}
