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
        var r = $resource('/:action/:arg2/:arg3/:arg4/:arg5', {
            action: '@action',
            arg2: '@arg2',
            arg3: '@arg3',
            arg4: '@arg4',
            arg5: '@arg5'
        }, {
            get: {method: 'GET', isArray: false},
            post: {method: 'POST', isArray: false}
        });

        return {
            get: r.get,
            post: r.post,

            login: function(username, password) {
                return $http.post('/.json_login/', {username: username, password:password});
            },
            logout: function() {
                return $http.get('/.json_logout/');
            }
        };

    });