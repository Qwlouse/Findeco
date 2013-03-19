'use strict';
/* Services */


angular.module('FindecoUserService', [])
    .factory('FindecoUserService', function () {
        var data = {};
        return {
            get: function() {
                return data;
            },
            set: function(d){data = d;},
            isLoggedIn: function() {
                return !angular.Object.equals({},data);
            }
        };
    });