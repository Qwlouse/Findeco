'use strict';
/* Controllers */

function FindecoNavigationCtrl($scope) {
    $scope.calculateNavigationEntries = function () {
        var pathParts = TheLocator.getPathParts();
        var navEntries = [];
        var pathSoFar = "/#/";

        for (var i = 0; i < pathParts.length; ++i) {
            pathSoFar += pathParts[i] + '/';
            navEntries.push({name:pathParts[i], path:pathSoFar});
        }
        return navEntries;
    }

    $scope.navigationEntries = $scope.calculateNavigationEntries();

    $scope.$on('$locationChangeSuccess', function (event, newLoc, oldLoc){
        $scope.navigationEntries = $scope.calculateNavigationEntries();
    });
}

FindecoNavigationCtrl.$inject = ['$scope', '$location'];