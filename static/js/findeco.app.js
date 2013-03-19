'use strict';
/* App Module */

angular.module('Findeco', ['FindecoService'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/home', {templateUrl: 'static/partials/home.html', controller: FindecoDefaultCtrl}).
            otherwise({templateUrl: 'static/partials/default.html', controller: FindecoDefaultCtrl});
    }]);