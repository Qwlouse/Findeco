'use strict';
/* Controllers */

function FindecoUserCtrl($scope, $location, FindecoService, FindecoUserService) {
    $scope.data = FindecoUserService.data;

    $scope.login = function () {
        FindecoUserService.data.content = FindecoService.login($scope.username, $scope.password).success(function (data) {
            FindecoUserService.data.isLoggedIn = true;
            $location.path('/');
        });
    };

    $scope.logout = function() {
        FindecoService.logout().success(function() {
            FindecoUserService.data.isLoggedIn = false;
            FindecoUserService.data.content = {};
            $location.path('/');
        });
    };

    FindecoUserService.initialize();
}

FindecoUserCtrl.$inject = ['$scope', '$location', 'FindecoService', 'FindecoUserService'];