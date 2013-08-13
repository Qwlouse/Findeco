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

function FindecoNewsCtrl($scope, Backend, User) {
    $scope.allNodesList = [];
    $scope.followedNodesList = [];
    $scope.ownNodesList = [];

    $scope.user = User;
    $scope.username = User.displayName;
    $scope.rsskey = User.rsskey;

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
            setAuthorForAllBlogs($scope.allNodesList);
            setAuthorForAllBlogs($scope.followedNodesList);
            setAuthorForAllBlogs($scope.ownNodesList);
        });
    };

    $scope.updateAllNodes = function (oldType, oldID) {
        var type = 'newer';
        var id = 0;
        if ($scope.allNodesList[0] != undefined) {
            id = $scope.allNodesList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.isLoadingNewsForAllNodes = true;
        Backend.loadMicroblogging($scope.allNodesList, ':collectionAll', type, id).success(function() {
        	setAuthorForAllBlogs($scope.allNodesList);
        	$scope.isLoadingNewsForAllNodes = false;
       });
    };

    $scope.updateFollowedNodes = function (oldType, oldID) {
        var type = 'newer';
        var id = 0;
        if ($scope.followedNodesList[0] != undefined) {
            id = $scope.followedNodesList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.isLoadingNewsForFollowedNodes=true;
        Backend.loadMicroblogging($scope.followedNodesList, ':collection', type, id).success(function() {
        	setAuthorForAllBlogs($scope.followedNodesList);
        	
        	$scope.isLoadingNewsForFollowedNodes=false;
        });
    };
    $scope.updateOwnNodes = function (oldType, oldID) {
        var type = 'newer';
    	var id = 0;
        if ($scope.ownNodesList[0] != undefined) {
            id = $scope.ownNodesList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.isLoadingNewsForOwnNodes=true;
        Backend.loadMicroblogging($scope.ownNodesList, ':collectionAuthor', type, id).success(function() {
        	setAuthorForAllBlogs($scope.ownNodesList);
        	$scope.isLoadingNewsForOwnNodes=false;	
        });
    };

    $scope.submit = function () {
        // todo: on which path to microblog?
        var path = "";
        Backend.storeMicroblogPost(path, $scope.microblogText).success(function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.$watch('username', function () {
        if ($scope.username != "") {
 
            $scope.updateAllNodes();
            $scope.updateFollowedNodes();
            $scope.updateOwnNodes();
        }
    });
    $scope.isLoading = function (col){
    	if (col =="timeline"){
    		return $scope.isLoadingNewsForAllNodes;
    	}
    	if (col =="newsForFollowedNodes"){
    		return $scope.isLoadingNewsForFollowedNodes;	
    	}
    	if (col =="newsForOwnNodes"){
    		return $scope.isLoadingNewsForOwnNodes;	
    	}
    	
    	return false;
    }
}

FindecoNewsCtrl.$inject = ['$scope', 'Backend', 'User'];