'use strict';
/* App Module */

angular.module('Findeco', ['FindecoService','FindecoUserService'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/home', {templateUrl: 'static/partials/home.html', controller: FindecoDefaultCtrl}).
            when('/login', {templateUrl: 'static/partials/login.html', controller: FindecoUserCtrl}).
            when('/register', {templateUrl: 'static/partials/register.html', controller: FindecoDefaultCtrl}).
            otherwise({templateUrl: 'static/partials/default.html', controller: FindecoDefaultCtrl});
    }]);