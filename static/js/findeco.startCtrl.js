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
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

'use strict';
/* Controllers */

function FindecoStartCtrl($scope, Backend, User) {
    $scope.followedUsersList = [];
    $scope.followedNodesList = [];
    $scope.ownNodesList = [];

    $scope.user = User;

    function setAuthorForAllBlogs(list) {
        for (var i = 0; i < list.length; ++i ) {
            var blog = list[i];
            blog.author = blog.authorGroup[0];
            blog.author.isFollowing = User.follows(blog.author.displayName);
            blog.author.path = blog.author.displayName;
        }
    }

    $scope.followUser = function (path, type) {
        return User.markUser(path, type).success(function() {
            setAuthorForAllBlogs($scope.followedUsersList);
            setAuthorForAllBlogs($scope.followedNodesList);
            setAuthorForAllBlogs($scope.ownNodesList);
        });
    };

    $scope.updateFollowedUsers = function () {
        var id = 0;
        if ($scope.followedUsersList[0] != undefined) {
            id = $scope.followedUsersList[0].microblogID;
        }
        Backend.loadMicroblogging($scope.followedUsersList, User.displayName, 'newer', id).success(function() {setAuthorForAllBlogs($scope.followedUsersList)});
    };
    $scope.updateFollowedNodes = function () {
        var id = 0;
        if ($scope.followedNodesList[0] != undefined) {
            id = $scope.followedNodesList[0].microblogID;
        }
        Backend.loadMicroblogging($scope.followedNodesList, ':collection', 'newer', id).success(function() {setAuthorForAllBlogs($scope.followedNodesList)});
    };
    $scope.updateOwnNodes = function () {
        var id = 0;
        if ($scope.ownNodesList[0] != undefined) {
            id = $scope.ownNodesList[0].microblogID;
        }
        Backend.loadMicroblogging($scope.ownNodesList, ':collectionAuthor', 'newer', id).success(function() {setAuthorForAllBlogs($scope.ownNodesList)});
    };

    $scope.submit = function () {
        // todo: on which path to microblog?
        var path = "";
        Backend.storeMicroblogPost(path, $scope.microblogText).success(function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.updateFollowedUsers();
    $scope.updateFollowedNodes();
    $scope.updateOwnNodes();
}

FindecoStartCtrl.$inject = ['$scope', 'Backend', 'User'];