'use strict';
/* Controllers */

function FindecoArgumentCtrl($scope, $location, FindecoService) {

    console.log("FindecoArgumentCtrl");

    $scope.path = TheLocator.getSanitizedArgumentFreePath();

    $scope.isTextLoaded = false;


    $scope.argumentList = [];
    $scope.getPath = function () {
        return TheLocator.getSanitizedArgumentFreePath();
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
        if ( TheLocator.isArgumentPath() ) {

        }
        FindecoService.loadArgument($scope.argumentList, $scope.path).success(function (data) {});
    };

    $scope.updateArgument();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];