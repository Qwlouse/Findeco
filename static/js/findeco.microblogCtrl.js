/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim                         *
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

function FindecoMicroblogCtrl($scope, Backend, User) {

    function containsUser(a, obj) {
        for (var i = 0; i < a.length; i++) {
            if (a[i].displayName === obj.displayName) {
                return 2;
            }
        }
        return 0;
    }

    function setAuthorForAllBlogs() {
        for (var i = 0; i < $scope.microbloggingList.length; ++i ) {
            var blog = $scope.microbloggingList[i];
            blog.author = blog.authorGroup[0];
            blog.author.isFollowing = containsUser(User.followees, blog.author);
            blog.author.path = blog.author.displayName;
        }
    }

    $scope.microbloggingList = [];
    $scope.user = User;

    $scope.followUser = function (path, type) {
        return User.markUser(path, type).success(setAuthorForAllBlogs);
    };

    $scope.updateMicrobloggingList = function () {
        Backend.loadMicroblogging($scope.microbloggingList, THELocatoooooooor.getSanitizedPath()).success(setAuthorForAllBlogs);
    };

    $scope.submit = function () {
        // TODO: Cross-site-scripting protection!
        if ($scope.microblogText.length <= 0) return;
        Backend.storeMicroblogPost(THELocatoooooooor.getSanitizedPath(), $scope.microblogText).success(function () {
            $scope.updateMicrobloggingList();
            $scope.microblogText = '';
        });
    };

    $scope.updateMicrobloggingList();


}

FindecoMicroblogCtrl.$inject = ['$scope', 'Backend', 'User'];