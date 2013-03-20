'use strict';
/* Controllers */

function FindecoDefaultCtrl($scope, $location, FindecoService) {
    $scope.path = TheLocator.getSanitizedPath();

    $scope.isTextLoaded = false;

    $scope.indexList = {};
    $scope.paragraphList = {};

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
        $scope.paragraphList = FindecoService.loadText($scope.path).success( function () {
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateIndex = function () {
        $scope.indexList = FindecoService.loadIndex($scope.path).success(function (data) {
            if ( angular.equals(data.loadIndexResponse, []) ) {
                $scope.updateParagraphList();
            }
        });
    };

    $scope.updateIndex();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];