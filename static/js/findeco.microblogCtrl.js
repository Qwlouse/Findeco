'use strict';
/* Controllers */

function FindecoMicroblogCtrl($scope, FindecoService) {
    $scope.microbloggingList = FindecoService.get({action: '.json_loadMicroblogging', arg2: '0', arg3: 'newer'});

    $scope.submit = function () {
        FindecoService.post({action: '.json_storeMicroblogPost/', 'microblogText': $scope.testinput}, function() {
            $scope.microbloggingList = FindecoService.get({action: '.json_loadMicroblogging', arg2: '0', arg3: 'newer'});
        });
    };
}