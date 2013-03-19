'use strict';
/* Controllers */

function FindecoUserCtrl($scope, $location, FindecoService, FindecoUserService) {
    $scope.login = function () {
        FindecoService.post({action: '.json_login/', 'username': $scope.username, 'password': $scope.password}, function (data) {
            FindecoUserService.data.isLoggedIn = true;
            FindecoUserService.data.content = data.loginResponse;
            $location.path('/');
        });
    };

    $scope.$on('logout', function () {
        FindecoService.get({action: '.json_logout/'}, function (data) {
            FindecoUserService.data.isLoggedIn = false;
            FindecoUserService.data.content = {};
            $location.path('/');
        });
    });
}

FindecoUserCtrl.$inject = ['$scope', '$location', 'FindecoService', 'FindecoUserService'];