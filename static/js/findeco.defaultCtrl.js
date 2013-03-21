'use strict';
/* Controllers */

function FindecoDefaultCtrl($scope, $location, FindecoService) {
    console.log("FindecoDefaultCtrl", FindecoService);
    $scope.path = TheLocator.getSanitizedPath();

    $scope.isTextLoaded = false;

    $scope.graphData = [{newFollows: 2, authorGroup: [{followers: [], displayName: "Beschlossenes Programm", followees: [], description: ""}], path: "Wahlprogramm_BTW.1/Urheberrecht.1", spamFlags: 0, follows: 2, originGroup: [], unFollows: 0}, {newFollows: 2, authorGroup: [{followers: [], displayName: "ulf", followees: [], description: ""}], path: "Wahlprogramm_BTW.1/Urheberrecht.2", spamFlags: 0, follows: 2, originGroup: [], unFollows: 0}, {newFollows: 1, authorGroup: [{followers: [], displayName: "ulf", followees: [], description: ""}], path: "Wahlprogramm_BTW.1/Urheberrecht.3", spamFlags: 0, follows: 1, originGroup: [], unFollows: 0}, {newFollows: 1, authorGroup: [{followers: [], displayName: "ulf", followees: [], description: ""}], path: "Wahlprogramm_BTW.1/Urheberrecht.4", spamFlags: 0, follows: 2, originGroup: ["Wahlprogramm_BTW.1/Urheberrecht.3"], unFollows: 0}, {newFollows: 1, authorGroup: [{followers: [], displayName: "timo", followees: [], description: ""}], path: "Wahlprogramm_BTW.1/Urheberrecht.5", spamFlags: 1, follows: 1, originGroup: ["Wahlprogramm_BTW.1/Urheberrecht.4"], unFollows: 2}];
    $scope.indexList = [];
    $scope.paragraphList = [];
    $scope.getPath = function (p) {
        return TheLocator.getSanitizedPath(p);
    };

    $scope.parse = function (text, shortTitle) {
        return Parser.parse(text, shortTitle, true);
    };

    $scope.relocateRelativeTo = function (shortTitle, index) {
        var path = $scope.path;
        if ($scope.path == '/') {
            path = '';
        }
        $location.path(TheLocator.getSanitizedPath(shortTitle + '.' + index));
    };

    $scope.updateParagraphList = function () {
        FindecoService.loadText($scope.paragraphList, $scope.path).success(function () {
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateIndex = function () {
        /*FindecoService.loadIndex($scope.indexList, $scope.path).success(function (data) {
            if (angular.equals(data.loadIndexResponse, [])) {
                $scope.updateParagraphList();
            }
        });*/
    };

    $scope.updateIndex();
}

FindecoDefaultCtrl.$inject = ['$scope', '$location', 'FindecoService'];