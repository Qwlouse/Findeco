'use strict';
/* Services */


angular.module('FindecoService', ['ngResource'])
    .factory('FindecoService', function ($resource) {
        return $resource('/:action/:arg2/:arg3/:arg4/:arg5', {
            action: '@action',
            arg2: '@arg2',
            arg3: '@arg3',
            arg4: '@arg4',
            arg5: '@arg5'
        }, {
            get: {method: 'GET', isArray: false},
            post: {method: 'POST', isArray: false}
        });
    });