'use strict';
/* Controllers */

function FindecoMicroblogCtrl($scope, FindecoService) {
    $scope.microbloggingList = [];
    $scope.updateMicrobloggingList = function () {
        FindecoService.loadMicroblogging($scope.microbloggingList, TheLocator.getSanitizedPath());
    };

    $scope.submit = function () {
        // TODO: Cross-site-scripting protection!
        FindecoService.storeMicroblogPost(TheLocator.getSanitizedPath(), $scope.microblogText).success(function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.updateMicrobloggingList();
}

FindecoMicroblogCtrl.$inject = ['$scope', 'FindecoService'];