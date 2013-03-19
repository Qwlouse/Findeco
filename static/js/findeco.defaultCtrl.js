'use strict';
/* Controllers */

function FindecoDefaultCtrl($scope, FindecoService) {
    $scope.microbloggingList = FindecoService.get({action: '.json_loadMicroblogging', arg2: '0', arg3: 'newer'},function (data) {
        console.log(data);
        return data;
    });
}