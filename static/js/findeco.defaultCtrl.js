'use strict';
/* Controllers */

function FindecoDefaultCtrl($scope, $location, FindecoService) {
    $scope.path = TheLocator.getSanitizedPath();

    $scope.isTextLoaded = false;

    $scope.indexList = {};
    $scope.paragraphList = {};

    $scope.parse = function(text,shortTitle) {
        return Parser.parse(text,shortTitle,true);
    }

    $scope.relocateRelativeTo = function(shortTitle,index) {
        var path = $scope.path;
        if ( $scope.path == '/' ) {
            path = '';
        }
        $location.path(TheLocator.getSanitizedPath(shortTitle + '.' + index));
    };

    $scope.updateParagraphList = function(params) {

        if ( params == undefined ) {
            params = {action: '.json_loadText', arg2: $scope.path};
        }
        FindecoService.get(params, function (data) {
            $scope.isTextLoaded = true;
            $scope.paragraphList = data.loadTextResponse.paragraphs;
        });
    };

    $scope.updateIndex = function (params) {
        if ( params == undefined ) {
            params = {action: '.json_loadIndex', arg2: $scope.path};
        }
        FindecoService.get(params, function (data) {
            if ( angular.equals(data.loadIndexResponse,[]) ) {
                $scope.updateParagraphList();
            }
            $scope.indexList = data.loadIndexResponse;
        });
    }

    $scope.updateIndex();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];