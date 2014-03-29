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
/* Controllers */

function FindecoArgumentNewsCtrl($scope, Backend, User, $location) {
    $scope.user = User;

    $scope.markNode = function(markType, nodePath) {
        var markedNode = $scope.cards[0]['argument'];
        for (var i = 0; i < $scope.cards.length; i++) {
            if ($scope.cards[i]['argument'].path == nodePath) {
                markedNode = $scope.cards[i]['argument'];
            }
            if ($scope.cards[i]['node'].path == nodePath) {
                markedNode = $scope.cards[i]['node'];
            }
        }
        var markedNodeOldIsFollowing = markedNode.isFollowing;
        var markedNodeOldIsFlagging  = markedNode.isFlagging;
        var promise = Backend.markNode(markType, nodePath);
        promise.success(function () {
            for (var i = 0; i < $scope.cards.length; i++) {
                var card = $scope.cards[i];
                if (card['argument'].path == nodePath) {
                    if (markType == 'follow') {
                        card['argument'].isFollowing = 2;
                        if (markedNodeOldIsFollowing == 0) {
                            card['argument'].followingCount += 1;
                        }
                    }
                    if (markType == 'unfollow') {
                        card['argument'].isFollowing = 0;
                        if (markedNodeOldIsFollowing > 0) {
                            card['argument'].followingCount -= 1;
                        }
                    }
                    if (markType == 'spam') {
                        card['argument'].isFlagging = 1;
                        if (markedNodeOldIsFlagging == 0) {
                            card['argument'].flaggingCount += 1;
                        }
                    }
                    if (markType == 'notspam') {
                        card['argument'].isFlagging = 0;
                        if (markedNodeOldIsFlagging > 0) {
                            card['argument'].flaggingCount -= 1;
                        }
                    }
                }
                if (card['node'].path == nodePath) {
                    if (markType == 'follow') {
                        card['node'].isFollowing = 2;
                        if (markedNodeOldIsFollowing == 0) {
                            card['node'].followingCount += 1;
                        }
                    }
                    if (markType == 'unfollow') {
                        card['node'].isFollowing = 0;
                        if (markedNodeOldIsFollowing > 0) {
                            card['node'].followingCount -= 1;
                        }
                    }
                    if (markType == 'spam') {
                        card['node'].isFlagging = 1;
                        if (markedNodeOldIsFlagging == 0) {
                            card['node'].flaggingCount += 1;
                        }
                    }
                    if (markType == 'notspam') {
                        card['node'].isFlagging = 0;
                        if (markedNodeOldIsFlagging > 0) {
                            card['node'].flaggingCount -= 1;
                        }
                    }
                }
            }
        });
        return promise;
    };

    $scope.cards = [];
    Backend.loadArgumentNews($scope.cards);
}

FindecoArgumentNewsCtrl.$inject = ['$scope', 'Backend', 'User', '$location'];