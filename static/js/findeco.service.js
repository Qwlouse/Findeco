'use strict';
/* Services */


angular.module('FindecoService', ['ngResource'])
    .config(function ($httpProvider) {
        $httpProvider.defaults.transformRequest = function(data){
            if (data === undefined) {
                return data;
            }
            return $.param(data);
        };
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    })
    .factory('FindecoService', function ($resource, $http) {
        function addSuccessAndError(value, promise) {
            value.success = function(fn) {
                promise.success(fn);
                return value;
            };
            value.error = function(fn) {
                promise.error(fn);
                return value;
            };
        }

        function fillArray(array, attributes) {
            return function (data) {
                for (var i = 0; i < attributes.length; ++i) {
                    data = data[attributes[i]];
                }
                array.length = 0;
                angular.forEach(data, function(item) {
                    array.push(item);
                });
            }
        }

        return {
            login: function(username, password) {
                var userInfo = {};
                var promise = $http.post('/.json_login/', {username: username, password:password});
                promise.success(function (d) {
                    angular.copy(d.loginResponse, userInfo);
                });
                addSuccessAndError(userInfo, promise);
                return userInfo;
            },
            logout: function() {
                return $http.get('/.json_logout/');
            },

            loadUserSettings: function() {
                var userInfo = {};
                var promise = $http.get('.json_loadUserSettings');
                promise.success(function (d) {
                    angular.copy(d.loadUserSettingsResponse, userInfo);
                });
                addSuccessAndError(userInfo, promise);
                return userInfo;
            },

            loadMicroblogging: function(microblogList, path, type, id) {
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
                // var microblogList = [];
                var promise = $http.get(url).success(fillArray(microblogList, ['loadMicrobloggingResponse']));
                addSuccessAndError(microblogList, promise);
                return microblogList;
            },

            storeMicroblogPost: function(path, microblogText) {
                var pathComponents = ['/.json_storeMicroblogPost', path];
                var url = pathComponents.join('/');
                return $http.post(url, {microblogText: microblogText});
            },

            loadArgument: function(indexNodes, path) {
                var url = ['/.json_loadIndex', 'true', path].join('/');
                // var indexNodes = [];
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes, ['loadIndexResponse']));
                addSuccessAndError(indexNodes, promise);
                return indexNodes;
            },

            loadText: function(paragraphList, path) {
                var url = ['/.json_loadText', path].join('/');
                // var paragraphList = [];
                var promise = $http.get(url);
                promise.success(fillArray(paragraphList, ['loadTextResponse', 'paragraphs']));
                addSuccessAndError(paragraphList, promise);
                return paragraphList;
            },

            loadIndex: function(indexNodes, path) {
                var url = ['/.json_loadIndex', path].join('/');
                // var indexNodes = [];
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes, ['loadIndexResponse']));
                addSuccessAndError(indexNodes, promise);
                return indexNodes;

            }
        };

    });