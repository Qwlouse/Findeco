'use strict';
/* Controllers */

function FindecoArgumentCtrl($scope, $location, $routeParams, FindecoService) {
    console.log("FindecoArgumentCtrl", FindecoService);
    $scope.path = TheLocator.getSanitizedArgumentFreePath();
    $scope.argumentPath = TheLocator.getSanitizedPath();

    $scope.isTextLoaded = false;
    $scope.paragraphList = [];
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

    $scope.updateParagraphList = function() {

    };

    $scope.updateArgument = function () {
        FindecoService.loadText($scope.paragraphList, $scope.argumentPath).success( function () {
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateArgumentList = function () {
        FindecoService.loadArgument($scope.argumentList , $scope.path);
    };

    $scope.updateArgumentList();
    if ( TheLocator.isArgumentPath() ) {
        $scope.updateArgument();
    }
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', '$routeParams', 'FindecoService'];