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
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

'use strict';
/* Controllers */

function FindecoUserCtrl($scope, $location, User, $routeParams, Message) {
    $scope.user = User;
    $scope.userEmail = User.email;
    $scope.newDisplayName = User.displayName;
    $scope.followUser = User.markUser;

    $scope.login = function () {
        User.login($scope.username, $scope.password).success(function () {
            $location.path('/');
        });
    };

    $scope.logout = function () {
        User.logout().success(function () {
            $location.path('/');
        });
    };

    $scope.register = function () {
        if (($scope.password == undefined) || ($scope.mail == undefined) || ($scope.username == undefined)) {
            Message.send("error", "_accountFieldsMissing_");
            return "";
        }
        if ($scope.password != $scope.password2) {
            Message.send("error", "_accountPasswordsNotMatching_");
            return "";
        }

        if ($scope.TOS != true) {
            Message.send("error", "_accountTosNotChecked_");
            return "";
        }
        if ($scope.DPR != true) {

            Message.send("error", "_accountDprNotChecked_");
            return "";
        }
        User.register($scope.username, $scope.password, $scope.mail).success(function () {
            $location.path('/');
            Message.send("success", "_accountCheckEmails_");
        });
    };

    $scope.activate = function () {
        if (!($location.path().substr(1, 8) == "activate")) {
            return "";
        }
        User.activate($routeParams.param).success(function () {
            $location.path('/');
            Message.send("success", "_accountActivationFinished_");
        });
    };
    $scope.confirm = function () {
        if (!($location.path().substr(1, 7) == "confirm")) {
            return "";
        }
        User.confirm($routeParams.param).success(function () {
            $location.path('/');
            Message.send("success", "_accountRecoveryConfirmed_");
        });
    };


    $scope.recoverByMail = function () {
        User.recoverByMail($scope.mail).success(function () {
            $location.path('/');
            Message.send("success", "_accountRecoveryFinished_");
        });
    };

    $scope.recoverByUsername = function () {
        User.recoverByUsername($scope.username).success(function () {
            $location.path('/');
            Message.send("success", "_accountRecoveryFinished_");
        });
    };


    $scope.getActiveClass = function (path) {
        if ($location.path().substr(0, path.length) == path) {
            return "activeTab";
        } else {
            return "";
        }
    };

    $scope.searchSubmit = function () {
        $location.path('search/' + $scope.searchString);
    };

    $scope.storeUserEMail = function () {
        $scope.user.email = $scope.userEmail;
        $scope.storeUserSettings();
        $scope.userEmail = User.email;
    };

    $scope.storeNewDisplayName = function () {
        $scope.user.displayName = $scope.newDisplayName;
        $scope.storeUserSettings();
        $scope.newDisplayName = User.displayName;
    };

    $scope.storeUserSettings = function () {
        User.storeSettings().error(User.loadSettings);
    };

    $scope.changePassword = function () {
        if ($scope.password1 == $scope.password2) {
            User.changePassword($scope.password1);
        } else {
            Message.send("error", "_passwordsDidNotMatch_");
        }
    };

    $scope.deleteAccount = function () {
        if (confirm(Message.localize('_deleteAccountQuestion_'))) {
            User.deleteAccount().success(function () {
                User.logout();
                $location.path('/');
            });
        }
    };

    $scope.parse = function (text) {
        if (text != undefined && text.length > 0)
            return Parser.parse(text, null, true);
        return "";
    };

    $scope.activate();
    $scope.confirm();

}

FindecoUserCtrl.$inject = ['$scope', '$location', 'User', '$routeParams' , 'Message'];
