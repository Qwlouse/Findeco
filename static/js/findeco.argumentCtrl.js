'use strict';
/* Controllers */

function FindecoArgumentCtrl($scope, $location, $routeParams, FindecoService) {
    $scope.path = THELocatoooooooor.getSanitizedArgumentFreePath();
    $scope.argumentPath = THELocatoooooooor.getSanitizedPath();

    $scope.isTextLoaded = false;
    $scope.paragraphList = [];
    $scope.argumentList = [];


    $scope.getPath = function () {
        return THELocatoooooooor.getSanitizedArgumentFreePath();
    };

    $scope.parse = function(text,shortTitle) {
        return Parser.parse(text,shortTitle,true);
    };

    $scope.relocateRelativeTo = function(shortTitle,index) {
        var path = $scope.path;
        if ( $scope.path == '/' ) {
            path = '';
        }
        $location.path(THELocatoooooooor.getSanitizedPath(shortTitle + '.' + index));
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
    if ( THELocatoooooooor.isArgumentPath() ) {
        $scope.updateArgument();
    }
}

FindecoArgumentCtrl.$inject = ['$scope', '$location', '$routeParams', 'FindecoService'];