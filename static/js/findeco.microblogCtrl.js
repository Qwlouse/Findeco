'use strict';
/* Controllers */

function FindecoMicroblogCtrl($scope, FindecoService) {
    $scope.microbloggingList = [];
    $scope.updateMicrobloggingList = function () {
        $scope.microbloggingList = FindecoService.loadMicroblogging(TheLocator.getSanitizedPath()).success(function() {
            alert('HA!')
        });
    };

    $scope.submit = function () {
        FindecoService.post({action: '.json_storeMicroblogPost', arg2: TheLocator.getSanitizedPath(), 'microblogText': $scope.microblogText}, function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.updateMicrobloggingList();
}

FindecoMicroblogCtrl.$inject = ['$scope', 'FindecoService'];