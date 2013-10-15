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

function FindecoMicrobloggingNewsCtrl($scope, Backend, User) {
    $scope.timelineList = [];
    $scope.mentionsList = [];
    $scope.ownPostsList = [];

    $scope.user = User;
    $scope.username = User.displayName;

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
            setAuthorForAllBlogs($scope.timelineList);
            setAuthorForAllBlogs($scope.mentionsList);
            setAuthorForAllBlogs($scope.ownPostsList);
        });
    };

    $scope.updateTimeline = function (oldType, oldID) {
        var type = 'newer';
        var id = 0;
        if ($scope.timelineList[0] != undefined) {
            id = $scope.timelineList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.isLoadingTimeline =true;
        Backend.loadMicrobloggingTimeline($scope.timelineList, User.displayName, id, type).success(function() {
        	setAuthorForAllBlogs($scope.timelineList);
        	$scope.isLoadingTimeline =false;
       });
    };

    $scope.updateMentions = function (oldType, oldID) {
        var type = 'newer';
        var id = 0;
        if ($scope.mentionsList[0] != undefined) {
            id = $scope.mentionsList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.isLoadingMentions=true;
        Backend.loadMicrobloggingMentions($scope.mentionsList, User.displayName, id, type).success(function() {
        	setAuthorForAllBlogs($scope.mentionsList);
        	$scope.isLoadingMentions=false;
        });
    };

    $scope.updateOwnPosts = function (oldType, oldID) {
        var type = 'newer';
        var id = 0;
        if ($scope.ownPostsList[0] != undefined) {
            id = $scope.ownPostsList[0].microblogID;
        }

        if ( oldType != undefined && oldID != undefined ) {
            type = oldType;
            id = oldID;
        }
        $scope.isLoadingOwnPosts=true;
        Backend.loadMicrobloggingFromUser($scope.ownPostsList, User.displayName, id, type).success(function() {
        	setAuthorForAllBlogs($scope.ownPostsList);
        	$scope.isLoadingOwnPosts=false;
        });
    };

    $scope.submit = function () {
        // todo: on which path to microblog?
        var path = "";

        if ($scope.microblogText.length <= 0) return;
        Backend.storeMicroblogPost(path, $scope.microblogText).success(function () {
            $scope.updateTimeline();
            $scope.updateMentions();
            $scope.updateOwnPosts();
            $scope.microblogText = '';
        });
    };

    $scope.$watch('username', function () {
        if ($scope.username != "") {
 
            $scope.updateTimeline();
            $scope.updateMentions();
            $scope.updateOwnPosts();
        }
    });

    $scope.isLoading = function (col){
    	if (col =="timeline"){
    		return $scope.isLoadingTimeline;	
    	}
    	if (col =="mentions"){
    		return $scope.isLoadingMentions;
    	}
        if (col =="own"){
    		return $scope.isLoadingOwnPosts;
    	}
    	
    	return false;
    };

    $('.microblogInput').focus(function(){
        $(this).animate({height:'6em'});
    }).blur(function(){
        $(this).animate({height:'1.4em'});
    });
}

FindecoMicrobloggingNewsCtrl.$inject = ['$scope', 'Backend', 'User'];