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
            userSettings: {
                email: "",
                rsskey: "",
                followees: [],
                wantsMailNotification: false,
                helpEnabled: true,
                preferredLanguage: ""
            }
        };
        var data = empty_data;
        var userInfo = {
            isLoggedIn : false,
            isAdmin    : false,
            displayName: "",
            newDisplayName: "",
            description: "",
            email      : "",
            rsskey     : "",
            followees  : [],
            wantsMailNotification: false,
            helpEnabled: true,
            preferredLanguage: ""
        };
        userInfo.register = function (displayName, password, emailAddress) {
            return $http.post('/.accountRegistration/', {
                displayName: displayName,
                password: password,
                emailAddress: emailAddress});
        };
        userInfo.activate = function (activationKey) {
            return $http.post('/.accountActivation/', {activationKey: activationKey});
        };
        userInfo.confirm = function (activationKey) {
            return $http.post('/.accountResetConfirmation/', {activationKey: activationKey});
        };
        userInfo.confirmEmail = function (activationKey) {
            return $http.post('/.emailChangeConfirmation/', {activationKey: activationKey});
        };
        userInfo.recoverByMail = function (emailAddress) {
            return $http.post('/.accountResetRequestByMail/',
                {emailAddress: emailAddress});
        };
        userInfo.recoverByUsername = function (displayName) {
            return $http.post('/.accountResetRequestByName/',
                {displayName: displayName});
        };
        userInfo.login = function (username, password) {
            var promise = $http.post('/.login/', {username: username, password: password});
            promise.success(function (d) {
                data = d.loginResponse;
                userInfo.isLoggedIn = true;
                userInfo.displayName = data.userInfo.displayName;
                userInfo.newDisplayName = data.userInfo.displayName;
                userInfo.description = data.userInfo.description;
                userInfo.rsskey = data.userSettings.rsskey;
                userInfo.email = data.userSettings.email;
                userInfo.followees = data.userSettings.followees;
                userInfo.wantsMailNotification = data.userSettings.wantsMailNotification;
                userInfo.helpEnabled = data.userSettings.helpEnabled;
                userInfo.preferredLanguage = data.userSettings.preferredLanguage;
                if (userInfo.displayName == "admin") {
                    userInfo.isAdmin = true;
                }
            });
            return promise;
        };
        userInfo.logout = function () {
            return $http.get('/.logout/').success(function () {
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
            var pathComponents = ['/.markUser', markType, displayName];
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
            if (userInfo.isLoggedIn) {
                var promise = $http.get('/.loadUserSettings/');
                promise.success(function (d) {
                    data = d.loadUserSettingsResponse;
                    userInfo.resetChanges();
                    userInfo.isLoggedIn = true;
                    userInfo.rsskey = data.userSettings.rsskey;
                    userInfo.followees = data.userSettings.followees;
                    userInfo.wantsMailNotification = data.userSettings.wantsMailNotification;
                    userInfo.helpEnabled = data.userSettings.helpEnabled;
                    userInfo.preferredLanguage = data.userSettings.preferredLanguage;
                    for (var i = 0; i < userInfo.followees.length; i++) {
                        userInfo.followees[i].isFollowing = 2;
                        userInfo.followees[i].path = userInfo.followees[i].displayName;
                    }
                    if (userInfo.displayName == "admin") {
                        userInfo.isAdmin = true;
                    }
                });
            }
        };
        userInfo.hasUnsavedChanges = function () {
            if (!userInfo.isLoggedIn) {
                return false;
            }
            return (userInfo.newDisplayName != userInfo.displayName) ||
                (userInfo.description != data.userInfo.description) ||
                (userInfo.email != data.userSettings.email) ||
                (userInfo.wantsMailNotification != data.userSettings.wantsMailNotification) ||
                (userInfo.helpEnabled != data.userSettings.helpEnabled) ||
                (userInfo.preferredLanguage != data.userSettings.preferredLanguage);
        };
        userInfo.resetChanges = function () {
            userInfo.displayName = data.userInfo.displayName;
            userInfo.newDisplayName = data.userInfo.displayName;
            userInfo.description = data.userInfo.description;
            userInfo.email = data.userSettings.email;
            userInfo.wantsMailNotification = data.userSettings.wantsMailNotification;
            userInfo.helpEnabled = data.userSettings.helpEnabled;
            userInfo.preferredLanguage = data.userSettings.preferredLanguage;
        };
        userInfo.storeSettings = function () {
            return $http.post('/.storeSettings/', {
                displayName: userInfo.displayName,
                description: userInfo.description,
                wantsMailNotification: userInfo.wantsMailNotification,
                helpEnabled: userInfo.helpEnabled,
                preferredLanguage: userInfo.preferredLanguage,
                email: userInfo.email}).success(function () {
                    data.userInfo.displayName = userInfo.displayName;
                    userInfo.newDisplayName = userInfo.displayName;
                    data.userInfo.description = userInfo.description;
                    data.userSettings.email = userInfo.email;
                    data.userSettings.wantsMailNotification = userInfo.wantsMailNotification;
                    data.userSettings.helpEnabled = userInfo.helpEnabled;
                    data.userSettings.preferredLanguage = userInfo.preferredLanguage;
            });
        };
        userInfo.changePassword = function (newPassword) {
            return $http.post('/.changePassword/', {password: newPassword});
        };
        userInfo.deleteAccount = function () {
            return $http.post('/.deleteUser/');
        };
        userInfo.isFollowing = function (name) {
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