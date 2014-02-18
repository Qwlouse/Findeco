/****************************************************************************************
 * Copyright (c) 2014 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
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

findecoApp.controller('FindecoMicroblogCtrl', function ($scope, $routeParams, $location, Backend, Navigator, User) {
    $scope.loadTarget = Navigator.argumentPath;
    if ( $routeParams.name != undefined ) {
        $scope.loadTarget = $routeParams.name;
    }

    function setAuthorForAllBlogs() {
        for (var i = 0; i < $scope.microbloggingList.length; ++i ) {
            var blog = $scope.microbloggingList[i];
            blog.author = blog.authorGroup[0];
            blog.author.isFollowing = User.isFollowing(blog.author.displayName);
            blog.author.path = blog.author.displayName;
        }
        $scope.MicrobloggingIsLoading = false;
    }

    $scope.$on('UserMarked', setAuthorForAllBlogs);

    $scope.microbloggingList = [];
    $scope.user = User;
    $scope.microblogText = "";

    $scope.followUser = function (type, path) {
        return User.markUser(type, path);
    };

    $scope.isLoading = function (){
    	return $scope.MicrobloggingIsLoading;
    };

    $scope.updateMicrobloggingList = function (oldType, oldID) {
        var type = 'newer';
        var id = 0;
        if ($scope.microbloggingList[0] != undefined) {
            id = $scope.microbloggingList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.MicrobloggingIsLoading = true;
        if (Navigator.type == 'user') {
            Backend.loadMicrobloggingFromUser($scope.microbloggingList, Navigator.userName, id, type).
                success(setAuthorForAllBlogs);
        } else {
            Backend.loadMicrobloggingForNode($scope.microbloggingList, $scope.loadTarget, id, type).
                success(setAuthorForAllBlogs);
        }
    };

    $scope.submit = function () {
        if ($scope.microblogText.length <= 0) return;
        var text = $scope.microblogText;
        if (Navigator.type == 'user') {
            text = "@" + Navigator.userName + ": " + text;
        }
        Backend.storeMicroblogging(Navigator.argumentPath, text).success(function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.UpdateIntervall = function () {
        if ($location.path() == $scope.path) {
            window.setTimeout(function () {
                $scope.UpdateIntervall();
                $scope.updateMicrobloggingList();
                $scope.MicrobloggingIsLoading = false;
            }, Math.floor((Math.random() * 10000) + 10000));
        }
    };

    $scope.path = $location.path();
    $scope.UpdateIntervall();

    
    $scope.updateMicrobloggingList();

    $('.microblogInput').focus(function(){
        $(this).animate({height:'6em'});
    }).blur(function(){
        $(this).animate({height:'1.4em'});
    });
});