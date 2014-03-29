/****************************************************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim, Johannes Merkert       *
 *                                                                                      *
 * This file is part of Findeco.                                                        *
 *                                                                                      *
 * Findeco is free software; you can redistribute it and/or modify it under             *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * Findeco is distributed in the hope that it will be useful, but WITHOUT ANY           *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * Findeco. If not, see <http://www.gnu.org/licenses/>.                                 *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

'use strict';
/* Controllers */

function FindecoArgumentCtrl($scope, Backend, User, TMP, Navigator) {
    $scope.nav = Navigator;
    $scope.tmp = TMP;
    $scope.user = User;

    $scope.markNode = function (markType, nodePath) {
        var argument = $scope.argumentList[0];
        for (var i = 0; i < $scope.argumentList.length; i++) {
            if ($scope.argumentList[i].path == nodePath) {
                argument = $scope.argumentList[i];
            }
        }
        var oldFollowState = argument.isFollowing;
        var promise = Backend.markNode(markType, nodePath);
        promise.success(function () {
            if (markType == 'follow' && oldFollowState == 0) {
                argument.followingCount += 1;
            }
            if (markType == 'unfollow' && oldFollowState > 0) {
                argument.followingCount -= 1;
            }
        });
        return promise;
    };

    $scope.argumentList = [];
    $scope.fullyShow = -1;

    $scope.showArgumentForPath = function () {
        for (var i = 0; i < $scope.argumentList.length; i++) {
            if (Navigator.argumentPath == $scope.argumentList[i].path) {
                $scope.fullyShow = $scope.argumentList[i].index;
            }
        }
        $scope.updateArgumentsWikiText($scope.fullyShow);
    };
    
    $scope.isLoading = function (){
    	return $scope.argumentIsLoading ;
    };

    $scope.createArgumentSlug = function (text) {
        var stringAddition = "";
        if (text.length > 140) {
            stringAddition = " ...";
        }
        return text.substr(0, 140) + stringAddition;
    };

    $scope.updateArgumentsWikiText = function (index) {
        for (var i = 0; i < $scope.argumentList.length; i++) {
            var arg = $scope.argumentList[i];
            if (index != arg.index) {
                arg.wikiText = $scope.createArgumentSlug(arg.text);
            } else {
                arg.wikiText = arg.text;
                $scope.fullyShow = arg.index;
            }
        }
        if (index >= 0) {
            window.setTimeout(function () {
                $(document.documentElement).animate(
                    {scrollTop: $('#argument' + index).offset().top},
                    'slow'
                );
            }, 0);
        }
    };
    
    function amendArguments() {
        for (var i = 0; i < $scope.argumentList.length; ++i) {
            var arg = $scope.argumentList[i];
            arg.path = $scope.nav.getPathForArgument(arg.argType, arg.index);
            arg.wikiText = $scope.createArgumentSlug(arg.text);
        }
        $scope.argumentIsLoading  = false;
        $scope.showArgumentForPath();
    }

    $scope.updateArgumentList = function () {
    	$scope.argumentIsLoading = true;
        Backend.loadArgument($scope.argumentList , $scope.nav.nodePath).success(amendArguments);
    };

    $scope.updateArgumentList();
    $scope.showArgumentForPath();
}

FindecoArgumentCtrl.$inject = ['$scope', 'Backend', 'User', 'TMP', 'Navigator'];