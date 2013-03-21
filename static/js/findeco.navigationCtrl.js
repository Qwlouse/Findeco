'use strict';
/* Controllers */

function FindecoNavigationCtrl($scope) {
    function get_navigation_entries() {
        var pathParts = TheLocator.getPathParts();
        var navEntries = [];
        var pathSoFar = "/#/";
        for (var i = 0; i < pathParts.length; ++i) {
            pathSoFar += pathParts[i] + '/';
            navEntries.push({name:pathParts[i], path:pathSoFar});
        }
        return navEntries;
    }

    $scope.navigationEntries = get_navigation_entries();

    $scope.$on('$locationChangeSuccess', function (event, newLoc, oldLoc){
        $scope.navigationEntries = get_navigation_entries();
    });
}

FindecoNavigationCtrl.$inject = ['$scope', '$location'];