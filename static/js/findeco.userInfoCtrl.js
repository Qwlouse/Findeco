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

function FindecoUserInfoCtrl($scope, Backend, $routeParams, User) {
    $scope.displayName = $routeParams.name.replace(/\//, '');

    $scope.follow = function (name, type) {
        Backend.markUser(name, type).success(function (data) {
            if (data.markUserResponse != undefined) {
                $scope.loadUserInfo();
            }
        });
    };

    $scope.loadUserInfo = function () {
        Backend.loadUserInfo($scope.displayName).success(function (data) {
            if (data.loadUserInfoResponse != undefined) {
                for (var l in data.loadUserInfoResponse.userInfo) {
                    $scope[l] = data.loadUserInfoResponse.userInfo[l];
                }
                $scope.following = false;
                for (var f in $scope.followees) {
                    if ($scope.followees[f].displayName == User.displayName) {
                        $scope.following = true;
                    }
                }
            }
        }).error(function () {
            $scope.displayName = "User " + $scope.displayName + " existiert nicht.";
        });
    };

    $scope.loadUserInfo();
}

FindecoUserInfoCtrl.$inject = ['$scope', 'Backend', '$routeParams', 'User'];