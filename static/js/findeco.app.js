'use strict';
/* App Module */

var findecoApp = angular.module('Findeco', ['FindecoService','FindecoUserService','localization'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/home', {templateUrl: 'static/partials/home.html', controller: FindecoDefaultCtrl}).
            when('/login', {templateUrl: 'static/partials/login.html', controller: FindecoUserCtrl}).
            otherwise({templateUrl: 'static/partials/default.html', controller: FindecoDefaultCtrl});
    }]);