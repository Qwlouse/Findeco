'use strict';
/* Controllers */

function FindecoUserCtrl($scope, $location, FindecoService, FindecoUserService) {
    $scope.login = function () {
        FindecoService.login($scope.username, $scope.password).success(function (data) {
            FindecoUserService.data.isLoggedIn = true;
            FindecoUserService.data.content = data.loginResponse;
            $location.path('/');
        });
    };

    $scope.$on('logout', function () {
        FindecoService.logout().success(function() {
            FindecoUserService.data.isLoggedIn = false;
            FindecoUserService.data.content = {};
            $location.path('/');
        });
    });
}

FindecoUserCtrl.$inject = ['$scope', '$location', 'FindecoService', 'FindecoUserService'];