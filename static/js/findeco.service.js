/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim                         *
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


/**
 *  Backend wraps the the JSON API to the backend.
 *  It provides easy to use functions like logout() or
 *  loadText(paragraphList, path).
 *
 *  Those functions return a $http promise object, on which you can add
 *  callbacks for success and failure like this:
 *
 *  Backend.logout().success( function (data, status, headers, config) {
 *      alert("goodbye");
 *  }).error( function (data, status, headers, config) {
 *      alert("logout failed");
 *  });
 *
 *  Those get called once the request finished.
 *
 *  When there is data to be returned, the first parameter to the function
 *  (typically suffixed with _out) is the object/array the function writes its
 *  results to.
 *
 *  This service is stateless.
 *
 **/
angular.module('FindecoServices', [])
    .config(function ($httpProvider) {
        // This tells the httpProvider to not send JSON in POST requests but
        // return the entries as post parameters instead
        $httpProvider.defaults.transformRequest = function (data) {
            if (data === undefined) {
                return data;
            }
            return $.param(data);
        };
        // using this https://github.com/angular/angular.js/commit/8155c3a29ea0eb14806913b8ac08ba7727e1969c
        // to rename X-XSRFToken to X-CSRFToken because Django expects it that way
        $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    })
    .factory('Backend', function ($http) {
        function fillArray(array, attributes) {
            return function (data) {
                for (var i = 0; i < attributes.length; ++i) {
                    data = data[attributes[i]];
                }
                array.length = 0;
                angular.forEach(data, function (item) {
                    array.push(item);
                });
            }
        }

        return {
            loadMicroblogging: function (microblogList_out, path, type, id) {
                var pathComponents = ['/.json_loadMicroblogging'];
                if (id != undefined) {
                    pathComponents.push(id);
                }
                if (type == undefined) {
                    type = "older"
                }
                pathComponents.push(type);
                pathComponents.push(path);
                var url = pathComponents.join('/');
                url = url.replace("//","/");
                var promise = $http.get(url);
                promise.success(fillArray(microblogList_out,
                    ['loadMicrobloggingResponse']));
                return promise;
            },

            markUser: function (displayName, markType) {
                var pathComponents = ['/.json_markUser', markType, displayName];
                var url = pathComponents.join('/');
                url = url.replace("//","/");
                return $http.post(url, {});
            },

            markNode: function (nodePath, markType) {
                var pathComponents = ['/.json_markNode', markType, nodePath];
                var url = pathComponents.join('/');
                url = url.replace("//","/");
                return $http.get(url);
            },

            storeMicroblogPost: function (path, microblogText) {
                var pathComponents = ['/.json_storeMicroblogPost', path];
                var url = pathComponents.join('/');
                //url = url.replace("//","/");
                return $http.post(url, {microblogText: microblogText});
            },

            storeText: function (path, params) {
                var pathComponents = ['/.json_storeText', path];
                var url = pathComponents.join('/');
                url = url.replace("//","/");
                return $http.post(url, params);
            },

            loadArgument: function (indexNodes_out, path) {
                var url = ['/.json_loadArgumentIndex', path].join('/');
                url = url.replace("//","/");
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes_out,
                    ['loadArgmumentIndexResponse']));
                return promise;
            },

            loadText: function (paragraphList_out, path) {
                var url = ['/.json_loadText', path].join('/');
                url = url.replace("//","/");
                var promise = $http.get(url);
                promise.success(fillArray(paragraphList_out,
                    ['loadTextResponse', 'paragraphs']));
                return promise;
            },

            loadUserInfo: function (user) {
                var url = ['/.json_loadUserInfo', user].join('/');
                url = url.replace("//","/");
                return $http.get(url);
            },

            loadNode: function (nodeInfo, path) {
                var url = ['/.json_loadNode', path].join('/');
                var promise = $http.get(url);
                promise.success( function (d) {
                    angular.copy(d.loadNodeResponse, nodeInfo);
                });
                return promise;
            },

            loadIndex: function (indexNodes_out, path) {
                var url = ['/.json_loadIndex', path].join('/');
                url = url.replace("//","/");
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes_out, ['loadIndexResponse']));
                return promise;
            },

            loadGraphData: function (graphData_out, path, graphType) {
                if (graphType == undefined) {
                    graphType = "full";
                }
                var url = ['/.json_loadGraphData', graphType, path].join('/');
                url = url.replace("//","/");
                var promise = $http.get(url);

                promise.success(fillArray(graphData_out, ['loadGraphDataResponse', 'graphDataChildren']));
                return promise;
            },

            search: function (searchResults, search_string) {
                var searchFields = "user_content_microblogging";
                var promise = $http.get('.json_search/'+searchFields+'/'+search_string);
                console.log("search in service called. Search string was "+search_string);

                promise.success(function (d) {
                    angular.copy(d.searchResponse, searchResults);
                });
            }
        };

    })
    .factory('User', function ($http, localize) {
    	var userInfo = {
            isLoggedIn: false,
            displayName: "",
            description: ""
        };
    	
        userInfo.register = function (displayName, password, emailAddress) {
            var promise = $http.post('/.json_accountRegistration/', {displayName: displayName, password: password, emailAddress:emailAddress});
            promise.success(function (d) {
            	console.log ('Please Check Mails');
            });
            return promise;
        };
        userInfo.activate = function (activationKey) {
            var promise = $http.post('/.json_accountActivation/', {activationKey: activationKey});
            promise.success(function (d) {
            	console.log ('Activated!!!');
            });
            return promise;
        };
        
        userInfo.login = function (username, password) {
            var promise = $http.post('/.json_login/', {username: username, password: password});
            promise.success(function (d) {
                var data = d.loginResponse.userInfo;
                userInfo.isLoggedIn = true;
                userInfo.displayName = data.displayName;
                userInfo.description = data.description;

            });
            return promise;
        };

        userInfo.logout = function () {
            return $http.get('/.json_logout/').success(function () {
                userInfo.isLoggedIn = false;
                userInfo.description = "";
                userInfo.displayName = "";
            });
        };

        userInfo.loadSettings = function () {
            var promise = $http.get('.json_loadUserSettings/');
            promise.success(function (d) {
                var data = d.loadUserSettingsResponse.userInfo;
                userInfo.isLoggedIn = true;
                userInfo.displayName = data.displayName;
                userInfo.description = data.description;
            });
            return promise;
        };

        userInfo.storeSettings = function () {
            return $http.post('.json_storeSettings/', {displayName: userInfo.displayName, description: userInfo.description});
        };

        userInfo.loadSettings();

        return userInfo;
    })
    .factory('TMP', function () {
        var tmp = {};
        return tmp;
    })
    .factory('Message', function () {
        var tmp = {messageList: []};

        tmp.send = function (type, message) {
            this.messageList.push({type: type, msg: message});
        }

        return tmp;
    })
;
