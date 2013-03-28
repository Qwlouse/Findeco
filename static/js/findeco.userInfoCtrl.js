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

function FindecoUserInfoCtrl($scope, Backend, $routeParams, User) {
    $scope.user = User;
    var name = $routeParams.name.replace(/\//, '');
    $scope.displayUser = {
        name: name,
        path: name,
        exists: false,
        isFollowing: User.follows(name)
    };

    $scope.followUser = User.markUser;

    $scope.loadUserInfo = function () {
        $scope.userExists = false;
        Backend.loadUserInfo(name).success(function (data) {
            $scope.displayUser.exists = true;
            $scope.displayUser.description = data.loadUserInfoResponse.userInfo.description;

        }).error(function () {
            $scope.displayUser.exists = false;
            $scope.displayUser.name = 'User "' + name + '" existiert nicht.';
        });
    };

    $scope.parse = function (text) {
        if ( text != undefined && text.length > 0 )
            return Parser.parse(text, null, true);
        return "";
    };

    $scope.loadUserInfo();
}

FindecoUserInfoCtrl.$inject = ['$scope', 'Backend', '$routeParams', 'User'];