'use strict';
/* Controllers */

function FindecoDefaultCtrl($scope, $location, FindecoService) {
    $scope.path = TheLocator.getPath();

    $scope.indexList = {};
    $scope.paragraphList = {};

    $scope.parse = function(text,shortTitle) {
        console.log("test");
        return Parser.parse(text,shortTitle,true);
    }

    $scope.relocateRelativeTo = function(shortTitle,index) {
        var path = $scope.path;
        if ( $scope.path == '/' ) {
            path = '';
        }
        $location.path(path + '/' + shortTitle + '.' + index);
    };

    $scope.updateParagraphList = function(params) {

        if ( params == undefined ) {
            params = {action: '.json_loadText', arg2: $scope.path};
        }
        FindecoService.get(params, function (data) {
            $scope.paragraphList = data.loadTextResponse.paragraphs;
        });
    };

    $scope.updateIndex = function (params) {
        if ( params == undefined ) {
            params = {action: '.json_loadIndex', arg2: $scope.path};
        }
        FindecoService.get(params, function (data) {
            $scope.indexList = data.loadIndexResponse;
        });
    }

    $scope.updateIndex();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];