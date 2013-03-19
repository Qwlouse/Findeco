'use strict';
/* Services */


angular.module('FindecoUserService', [])
    .factory('FindecoUserService', function () {
        return {isLoggedIn:false};
    });