'use strict';
/* Controllers */

function FindecoMenuCtrl($scope, $rootScope, $location, FindecoUserService) {
    FindecoUserService.initialize();

    $scope.data = FindecoUserService.data;

    $scope.logout = function() {
        $rootScope.$broadcast('logout');
    }
}

FindecoMenuCtrl.$inject = ['$scope', '$rootScope', '$location', 'FindecoUserService'];