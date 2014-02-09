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
angular.module('FindecoUserService', [])
    .factory('User', function ($http, $rootScope) {
        var empty_data = {
            userInfo    : {description: "", displayName: ""},
            userSettings: {email: "",  rsskey: "", followees: [],
                           wantsMailNotification:false}
        };
        var data = empty_data;
        var userInfo = {
            isLoggedIn : false,
            isAdmin    : false,
            displayName: "",
            description: "",
            email      : "",
            rsskey     : "",
            followees  : [],
            wantsMailNotification : false
        };
        userInfo.register = function (displayName, password, emailAddress) {
            return $http.post('/.json_accountRegistration/', {
                displayName: displayName,
                password: password,
                emailAddress: emailAddress});
        };
        userInfo.activate = function (activationKey) {
            return $http.post('/.json_accountActivation/', {activationKey: activationKey});
        };
        userInfo.confirm = function (activationKey) {
            return $http.post('/.json_accountResetConfirmation/', {activationKey: activationKey});
        };
        userInfo.confirmEmail = function (activationKey) {
            return $http.post('/.json_emailChangeConfirmation/', {activationKey: activationKey});
        };
        userInfo.recoverByMail = function (emailAddress) {
            return $http.post('/.json_accountResetRequestByMail/',
                {emailAddress: emailAddress});
        };
        userInfo.recoverByUsername = function (displayName) {
            return $http.post('/.json_accountResetRequestByName/',
                {displayName: displayName});
        };
        userInfo.login = function (username, password) {
            var promise = $http.post('/.json_login/', {username: username, password: password});
            promise.success(function (d) {
                var data = d.loginResponse;
                userInfo.isLoggedIn = true;
                userInfo.displayName = data.userInfo.displayName;
                userInfo.description = data.userInfo.description;
                userInfo.rsskey = data.userSettings.rsskey;
                userInfo.email = data.userSettings.email;
                userInfo.followees = data.userSettings.followees;
                userInfo.wantsMailNotification = data.userSettings.wantsMailNotification;
                if (userInfo.displayName == "admin") {
                    userInfo.isAdmin = true;
                }
            });
            return promise;
        };
        userInfo.logout = function () {
            return $http.get('/.json_logout/').success(function () {
                userInfo.isLoggedIn = false;
                userInfo.displayName = "";
                userInfo.description = "";
                userInfo.rsskey = "";
                userInfo.followees = [];
                userInfo.email = "";
                userInfo.isAdmin = false;
                data = empty_data;
            });
        };
        userInfo.markUser = function (markType, displayName) {
            var pathComponents = ['/.json_markUser', markType, displayName];
            var url = pathComponents.join('/');
            url = url.replace("//", "/");
            return $http.post(url, {}).success(function (d) {
                userInfo.followees = d.markUserResponse.followees;
                for (var i = 0; i < userInfo.followees.length; i++) {
                    userInfo.followees[i].isFollowing = 2;
                    userInfo.followees[i].path = userInfo.followees[i].displayName;
                }
                $rootScope.$broadcast('UserMarked');
            });
        };
        userInfo.loadSettings = function () {
            var promise = $http.get('/.json_loadUserSettings/');
            promise.success(function (d) {
                data = d.loadUserSettingsResponse;
                userInfo.resetChanges();
                userInfo.isLoggedIn = true;
                userInfo.rsskey = data.userSettings.rsskey;
                userInfo.followees = data.userSettings.followees;
                userInfo.wantsMailNotification = data.userSettings.wantsMailNotification;

                for (var i = 0; i < userInfo.followees.length; i++) {
                    userInfo.followees[i].isFollowing = 2;
                    userInfo.followees[i].path = userInfo.followees[i].displayName;
                }
                if (userInfo.displayName == "admin") {
                    userInfo.isAdmin = true;
                }
            });
        };
        userInfo.hasUnsavedChanges = function () {
            if (!userInfo.isLoggedIn) {
                return false;
            }
            return (userInfo.displayName != data.userInfo.displayName) ||
                (userInfo.description != data.userInfo.description) ||
                (userInfo.email != data.userSettings.email) ||
                (userInfo.wantsMailNotification != data.userSettings.wantsMailNotification);
        };
        userInfo.resetChanges = function () {
            userInfo.displayName = data.userInfo.displayName;
            userInfo.description = data.userInfo.description;
            userInfo.email = data.userSettings.email;
            userInfo.wantsMailNotification = data.userSettings.wantsMailNotification;
        };
        userInfo.storeSettings = function () {
            return $http.post('/.json_storeSettings/', {
                displayName: userInfo.displayName,
                description: userInfo.description,
                wantsMailNotification: userInfo.wantsMailNotification,
                email: userInfo.email});
        };
        userInfo.changePassword = function (newPassword) {
            return $http.post('/.json_changePassword/', {password: newPassword});
        };
        userInfo.deleteAccount = function () {
            return $http.post('/.json_deleteUser/');
        };
        userInfo.follows = function (name) {
            for (var i = 0; i < userInfo.followees.length; i++) {
                if (userInfo.followees[i].displayName == name) {
                    return userInfo.followees[i].isFollowing;
                }
            }
            return 0;
        };
        userInfo.loadSettings();
        return userInfo;
    });