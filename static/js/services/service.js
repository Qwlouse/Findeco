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

angular.module('FindecoServices', [])
    .config(function ($httpProvider) {
        // using this https://github.com/angular/angular.js/commit/8155c3a29ea0eb14806913b8ac08ba7727e1969c
        // to rename X-XSRFToken to X-CSRFToken because Django expects it that way
        $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/json; charset=UTF-8';
        $httpProvider.responseInterceptors.push('errorHandler');
    })
    .config(function ($locationProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
    })
    .factory('errorHandler', function ($q, Message) {
        return function (promise) {
            return promise.then(
                function (response) {
                    return response;
                },
                function (response) {
                    if (response.data.errorResponse != undefined) {
                        Message.send("error", response.data.errorResponse.errorID);  // TODO: what to do with this?
                    }
                    return $q.reject(response);
                }
            );
        }
    })
    .factory('Fesettings', function (Disclaimer, Boxes, Version, Sidebar, Greetingbox, ActivatedLanguages) {
        var settings = {};
        settings.version = Version;
        settings.disclaimer = Disclaimer;
        settings.boxes = Boxes;
        settings.sidebar = Sidebar;
        settings.greetingbox = Greetingbox;
        settings.activatedLanguages = ActivatedLanguages;
        return settings;
    })
    .factory('TMP', function () {
        var tmp = {};
        return tmp;
    })
    .factory('Message', function ($injector) {
        var tmp = {
            messageList: [],
            catchList  : {}
        };
        tmp.localize = function (string) {
            this.localizer = this.localizer || $injector.get('localize');
            return this.localizer.getLocalizedString(string);
        };
        tmp.send = function (type, message) {
            if (message == "_NotAuthenticated") {
                return "";
            }
            if (message.substr(0, 1) == "_") {
                message = this.localize(message);
            }
            if (this.catchList[message] != undefined) {
                this.catchList[message].push({type: type, msg: message});
            } else {
                this.messageList.push({type: type, msg: message});
            }
        };
        tmp.clear = function () {
            this.messageList = [];
        };
        tmp.catch = function (message) {
            this.catchList[message] = [];
            return this.catchList[message];
        };
        return tmp;
    })
    .service('Help', function ($rootScope, $http) {
        $rootScope.helpIsActive = true;
        var help = {
            isLoaded        : false,
            data            : [],
            helpText        : "",
            helpTitle       : "",
            moreLink        : "",
            setID           : function (x) {
                help.id = x;
                help.loadResourceFile();
                if ((help.data !== []) && (help.data.length > 0)) {
                    var i = 0, len = help.data.length;
                    for (; i < len; i++) {
                        if (help.data[i].key == help.id) {
                            help.helpText = help.data[i].description;
                            help.moreLink = help.data[i].more;
                            help.helpTitle = help.data[i].title;
                        }
                    }
                }
                $rootScope.$broadcast('change_Help', x);
                return true;
            },
            getID           : function (x) {
                return help.id;
            },
            setHelpStatus   : function (x) {
                $rootScope.helpIsActive = x;
                return true;
            },
            successCallback : function (data) {
                help.data = data;
                help.resourceFileLoaded = true;
            },
            loadResourceFile: function () {
                if (help.isLoaded == false) {
                    var url = '/static/resource-help.js';
                    $http({ method: "GET", url: url, cache: false }).success(help.successCallback).error(function () {
                        alert("Helptextfile not found")
                    });
                }
            }
        };
        return help;
    });
