'use strict';
/* Controllers */

function FindecoNavigationCtrl($scope) {
    $scope.calculateNavigationEntries = function () {
        var pathParts = THELocatoooooooor.getPathParts();
        var navEntries = [];
        var pathSoFar = "/#";

        var tmp = "";
        for (var i = 0; i < pathParts.length; ++i) {
            tmp = pathParts[i].split('.');
            pathSoFar += '/' + tmp[0] + '.' + tmp[1];
            navEntries.push({name: tmp[0] + '.' + tmp[1], path: pathSoFar});
        }
        if (THELocatoooooooor.isArgumentPath()) {
            pathSoFar += '.' + tmp[2] + '.' + tmp[3];
            navEntries.push({name: tmp[0] + '.' + tmp[1] + '.' + tmp[2] + '.' + tmp[3], path: '/#/argument' + pathSoFar.substr(2)});
        }
        return navEntries;
    }

    $scope.navigationEntries = $scope.calculateNavigationEntries();

    $scope.$on('$locationChangeSuccess', function (event, newLoc, oldLoc) {
        $scope.navigationEntries = $scope.calculateNavigationEntries();
    });
}

FindecoNavigationCtrl.$inject = ['$scope', '$location'];