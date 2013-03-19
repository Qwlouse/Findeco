'use strict';
/* Controllers */

function FindecoMicroblogCtrl($scope, FindecoService) {
    $scope.updateMicrobloggingList = function (params) {
        if ( params == undefined ) {
            params = {action: '.json_loadMicroblogging', arg2: '0', arg3: 'newer', arg4: TheLocator.getPath()};
        }
        FindecoService.get(params, function (data) {
            $scope.microbloggingList = data;
        });
    }

    $scope.submit = function () {
        FindecoService.post({action: '.json_storeMicroblogPost', arg2: TheLocator.getPath(), 'microblogText': $scope.microblogText}, function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.updateMicrobloggingList();
}

FindecoMicroblogCtrl.$inject = ['$scope', 'FindecoService'];