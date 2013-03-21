'use strict';
/* Controllers */

function FindecoDefaultCtrl($scope, $location, FindecoService) {

    console.log("FindecoDefaultCtrl");

    $scope.path = TheLocator.getSanitizedPath();

    $scope.isTextLoaded = false;

    $scope.indexList = [];
    $scope.paragraphList = [];
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

    $scope.updateParagraphList = function() {
        FindecoService.loadText($scope.paragraphList, $scope.path).success( function () {
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateIndex = function () {
        FindecoService.loadIndex($scope.indexList, $scope.path).success(function (data) {
            if ( angular.equals(data.loadIndexResponse, []) ) {
                $scope.updateParagraphList();
            }
        });
    };


    $scope.initialize = function() {
        if ( TheLocator.isArgumentPath() ) {
            $scope.updateParagraphList();
        } else {
            $scope.updateIndex();
        }
    }
    $scope.initialize();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];