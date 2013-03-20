'use strict';
/* Controllers */

function FindecoMicroblogCtrl($scope, FindecoService) {
    $scope.microbloggingList = [];
    $scope.updateMicrobloggingList = function () {
        $scope.microbloggingList = FindecoService.loadMicroblogging(TheLocator.getSanitizedPath());
    };

    $scope.submit = function () {
        FindecoService.storeMicroblogPost(TheLocator.getSanitizedPath(), $scope.microblogText).success(function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.updateMicrobloggingList();
}

FindecoMicroblogCtrl.$inject = ['$scope', 'FindecoService'];