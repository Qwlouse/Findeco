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

        var r = $resource('/:action/:arg2/:arg3/:arg4/:arg5', {
            action: '@action',
            arg2: '@arg2',
            arg3: '@arg3',
            arg4: '@arg4',
            arg5: '@arg5'
        }, {
            get: {method: 'GET', isArray: false},
            post: {method: 'POST', isArray: false},
            query: {method: 'GET', isArray: true}
        });

        return {
            get: r.get,
            post: r.post,

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

            loadMicroblogging: function(path, type, id) {
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
                var microblogList = [];
                var promise = $http.get(url).success(function(d) {
                    microblogList.length = 0;
                    angular.forEach(d.loadMicrobloggingResponse, function(item) {
                        microblogList.push(item);
                    });
                });
                addSuccessAndError(microblogList, promise);
                return microblogList;
            },

            storeMicroblogPost: function(path, microblogText) {
                var pathComponents = ['/.json_storeMicroblogPost', path];
                var url = pathComponents.join('/');
                return $http.post(url, {microblogText: microblogText});
            },

            loadText: function(path) {
                var url = ['/.json_loadText', path].join('/');
                var paragraphList = [];
                var promise = $http.get(url);
                promise.success(function(d) {
                    paragraphList.length = 0;
                    angular.forEach(d.loadTextResponse.paragraphs, function(item) {
                        paragraphList.push(item);
                    });
                });
                addSuccessAndError(paragraphList, promise);
                return paragraphList;
            }
        };

    });