'use strict';
/* Controllers */

function FindecoArgumentCtrl($scope, $location, FindecoService) {
    $scope.path = TheLocator.getSanitizedPath();

    $scope.isTextLoaded = false;


    $scope.argumentList = [];
    $scope.getPath = function (p) {
        return TheLocator.getSanitizedPath(p);
    };

    $scope.parse = function(text,shortTitle) {
        return Parser.parse(text,shortTitle,true);
    };

    $scope.relocateRelativeTo = function(shortTitle,index) {
        var path = $scope.path;
        if ( $scope.path == '/' ) {
            path = '';
        }
        $location.path(TheLocator.getSanitizedPath(shortTitle + '.' + index));
    };

    $scope.updateArgument = function () {
        FindecoService.loadArgument($scope.argumentList, $scope.path).success(function (data) {});
    };

    $scope.updateArgument();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];