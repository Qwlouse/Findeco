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
                        Message.send("error", response.data.errorResponse.errorID);
                        delete response.data.errorResponse;
                    }
                    return $q.reject(response);
                }
            );
        }
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

        function filterMicroblogging(data, microblogList_out) {
            angular.forEach(data['loadMicrobloggingResponse'], function (item) {
                var flag = false;
                angular.forEach(microblogList_out, function (oldItem) {
                    if (oldItem.microblogID == item.microblogID) {
                        flag = true;
                    }
                });
                if (flag == false) {
                    microblogList_out.push(item);
                }
            });
            microblogList_out = microblogList_out.sort(function (a, b) {
                return b.microblogID - a.microblogID;
            });
        }

        function addIdTypeAndGetPromise(path, id, type) {
            if (id != undefined && id != 0) {
                    path += id + '/';
                }
                if (type == undefined) {
                    type = "newer";
                }
                var promise = $http.get(path + type);
                promise.success(function (data) {
                    filterMicroblogging(data, microblogList_out);
                });
                return promise;
        }

        return {
       	 	loadAnnounce: function () {
       	 	 var promise = $http.get('/static/externaljson/info.json');
       	 	 return promise;
       	 	
            },
            loadMicrobloggingForFollowedNodes: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingForFollowedNodes/' + name + '/';
                return addIdTypeAndGetPromise(path, id, type);
            },
            loadMicrobloggingForAllNodes: function (microblogList_out, id, type) {
                var path = '/.loadMicrobloggingAll/';
                return addIdTypeAndGetPromise(path, id, type);
            },
            loadMicrobloggingForAuthoredNodes: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingForAuthoredNodes/' + name + '/';
                return addIdTypeAndGetPromise(path, id, type);
            },
            loadMicroblogging: function (microblogList_out, path, type, id, mentions, own) {
                var pathComponents = ['/.json_loadMicroblogging'];
                if (mentions != undefined && mentions == true) {
                    pathComponents.push('mentions');
                }
                if (own != undefined && own == true) {
                    pathComponents.push('own');
                }
                if (id != undefined && id != 0) {
                    pathComponents.push(id);
                }
                if (type == undefined) {
                    type = "newer"
                }
                pathComponents.push(type);
                pathComponents.push(path);
                var url = pathComponents.join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);
                promise.success(function (data) {
                    angular.forEach(data['loadMicrobloggingResponse'], function (item) {
                        var flag = false;
                        angular.forEach(microblogList_out, function (oldItem) {
                            if (oldItem.microblogID == item.microblogID) {
                                flag = true;
                            }
                        });
                        if (flag == false) {
                            microblogList_out.push(item);
                        }
                    });
                    microblogList_out = microblogList_out.sort(function (a, b) {
                        return b.microblogID - a.microblogID;
                    });
                });
                return promise;
            },

            markNode: function (nodePath, markType) {
                var pathComponents = ['/.json_markNode', markType, nodePath];
                var url = pathComponents.join('/');
                url = url.replace("//", "/");
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
                url = url.replace("//", "/");
                return $http.post(url, params);
            },

            loadArgument: function (indexNodes_out, path) {
                var url = ['/.json_loadArgumentIndex', path].join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes_out,
                    ['loadArgumentIndexResponse']));
                return promise;
            },

            loadText: function (paragraphList_out, path) {
                var url = ['/.json_loadText', path].join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);
                promise.success(fillArray(paragraphList_out,
                    ['loadTextResponse', 'paragraphs']));
                return promise;
            },

            loadUserInfo: function (user) {
                var url = ['/.json_loadUserInfo', user].join('/');
                url = url.replace("//", "/");
                return $http.get(url);
            },

            loadNode: function (nodeInfo, path) {
                var url = ['/.json_loadNode', path].join('/');
                var promise = $http.get(url);
                promise.success(function (d) {
                    angular.copy(d.loadNodeResponse, nodeInfo);
                });
                return promise;
            },

            loadIndex: function (indexNodes_out, path) {
                var url = ['/.json_loadIndex', path].join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes_out, ['loadIndexResponse']));
                return promise;
            },

            loadGraphData: function (graphData_out, path, graphType) {
                if (graphType == undefined) {
                    graphType = "full";
                }
                var url = ['/.json_loadGraphData', graphType, path].join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);

                promise.success(fillArray(graphData_out, ['loadGraphDataResponse', 'graphDataChildren']));
                return promise;
            },

            search: function (searchResults, search_string) {
                var searchFields = "user_content_microblogging";
                var promise = $http.get('/.json_search/' + searchFields + '/' + search_string);

                promise.success(function (d) {
                    angular.copy(d.searchResponse, searchResults);
                });
            }
        };

    })
    .factory('User', function ($http) {
        var data = {
            userInfo : false,
            userSettings : false
        };

        var userInfo = {
            isLoggedIn: false,
            displayName: "",
            description: "",
            email: "",
            rsskey:"",
            followees: []
        };

        userInfo.register = function (displayName, password, emailAddress) {
            return $http.post('/.json_accountRegistration/', {displayName: displayName, password: password, emailAddress: emailAddress});
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
            var promise = $http.post('/.json_accountResetRequestByMail/', {emailAddress: emailAddress});
            promise.success(function (d) {

            });
            return promise;
        };

        userInfo.recoverByUsername = function (displayName) {
            var promise = $http.post('/.json_accountResetRequestByName/', {displayName: displayName});
            promise.success(function (d) {

            });
            return promise;
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
            });
            return promise;
        };

        userInfo.logout = function () {
            return $http.get('/.json_logout/').success(function () {
                userInfo.isLoggedIn = false;
                userInfo.description = "";
                userInfo.displayName = "";
                userInfo.followees = [];
                userInfo.email = "";
                data.userInfo = false;
                data.userSettings = false;
            });
        };

        userInfo.markUser = function (displayName, markType) {
            var pathComponents = ['/.json_markUser', markType, displayName];
            var url = pathComponents.join('/');
            url = url.replace("//", "/");
            return $http.post(url, {}).success(function (d) {
                userInfo.followees = d.markUserResponse.followees;
                for (var i = 0; i < userInfo.followees.length; i++) {
                    userInfo.followees[i].isFollowing = 2;
                    userInfo.followees[i].path = userInfo.followees[i].displayName;
                }
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
                for (var i = 0; i < userInfo.followees.length; i++) {
                    userInfo.followees[i].isFollowing = 2;
                    userInfo.followees[i].path = userInfo.followees[i].displayName;
                }
                
            });
            return promise;
        };

        userInfo.isChanged = function () {
            if (! userInfo.isLoggedIn || !data.userInfo) {
                return false;
            }
            return (userInfo.displayName != data.userInfo.displayName) ||
                   (userInfo.description != data.userInfo.description) ||
                   (userInfo.email != data.userSettings.email);
        };

        userInfo.resetChanges = function () {
            userInfo.displayName = data.userInfo.displayName;
            userInfo.description = data.userInfo.description;
            userInfo.email = data.userSettings.email;
        };

        userInfo.storeSettings = function () {
            return $http.post('/.json_storeSettings/', {displayName: userInfo.displayName,
                description: userInfo.description, email: userInfo.email});
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
                    return 2;
                }
            }
            return 0;
        };

        userInfo.loadSettings();

        return userInfo;
    })
    .factory('TMP', function () {
        var tmp = {};
        return tmp;
    })
    .factory('Message', function ($injector) {
        var tmp = {
            messageList: [],
            catchList: {}
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
		
        tmp.catch = function (message) {
            this.catchList[message] = [];
            return this.catchList[message];
        };

        return tmp;
    })
    .factory('Navigator', function ($rootScope, $location) {
        var nodePattern = "[a-zA-Z][a-zA-Z0-9_-]{0,19}\\.[0-9]+";
        // TODO: disallow duplicated slashes
        var rootPath = new RegExp("^/*$");
        var nodePath =     new RegExp("/+(" + nodePattern + "/+)*(" + nodePattern + ")/*$");
        var argumentPath = new RegExp("/+(" + nodePattern + "/+)*(" + nodePattern + ")\\.(pro|neut|con)\\.[0-9]+/*$");
        var userPath = new RegExp("^/user/[a-zA-Z][a-zA-Z0-9-_]{0,19}/*$");

        function isNonEmpty(element, index, array) {
            return (element != "");
        }

        var location = {
            path : "",    // the full path but duplicate slashes are removed
            prefix : "",  // things before the node or user path like /create/argumentPro/ or /user/
            nodePath : "", // only the node path (parent for arguments, empty for users)
            argumentPath : "", // the full path to the argument or node if it isn't an argument
            userName : "", // user
            parts : [],
            entries : [],  // contains objects with name and path for every ancestor node
            type : "node"  // one of: root, node, arg, user, other
        };

        function normalizeSlashes(path) {
            return path.split("/").filter(isNonEmpty).join('/');
        }

        location.updatePath = function () {
            var path = $location.path();
            location.segments = $location.search();
            location.parts = path.split("/").filter(isNonEmpty);
            location.path = '/' + location.parts.join("/");
            location.prefix = "";
            location.nodePath = "";
            location.argumentPath = "";
            location.userName = "";
            location.entries = [];
            location.type = "";
            // find out the type of path
            if (path.match(rootPath)) {
                location.type = "root";
            } else if (path.match(nodePath)) {
                location.type = "node";
                location.prefix = normalizeSlashes(location.path.replace(nodePath, ''));
                location.nodePath = normalizeSlashes(nodePath.exec(location.path)[0]);
                location.argumentPath = location.nodePath;
            } else if (path.match(argumentPath)) {
                location.type = "arg";
                location.argumentPath = normalizeSlashes(argumentPath.exec(location.path)[0]);
                location.prefix = normalizeSlashes(location.path.replace(argumentPath, ''));
                location.nodePath = normalizeSlashes(location.argumentPath.replace(/\.(pro|con|neut)\.\d+\/?$/,''));
            } else if (path.match(userPath)) {
                location.type = "user";
                location.prefix = "user";
                location.userName = location.parts[1];
            } else {
                location.type = "other";
                location.prefix = location.parts[0];
            }
            // calculate entries
            var nodes = location.nodePath.split('/');
            var pathSoFar = "";
            for (var i = 0; i < nodes.length; ++i) {
                pathSoFar += '/' + nodes[i];
                location.entries.push({name : nodes[i], path : pathSoFar});
            }
            if (location.type == 'arg') {
                nodes = location.argumentPath.split('/');
                var arg_parts = nodes[nodes.length - 1].split('.');
                location.entries.push({name : arg_parts[2] + '.' + arg_parts[3], path : location.argumentPath});
            }
        };

        location.getPathForNode = function (shortTitle, index) {
            return normalizeSlashes(location.nodePath + '/' + shortTitle + '.' + index);
        };

        location.getPathForArgument = function (argType, index) {
            return normalizeSlashes(location.nodePath + '.' + argType + '.' + index);
        };

        location.getPathForUser = function (username) {
            return 'user/' + username;
        };

        location.changePath = function (newPath) {
            $location.path(newPath);
        };

        location.updatePath();
        $rootScope.$on('$routeChangeSuccess', location.updatePath);

        return location;
    })
;
