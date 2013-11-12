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

function FindecoMenuCtrl($scope, User, Navigator, Fesettings) {
    $scope.user = User;
    $scope.fesettings = Fesettings;
    $scope.logout = function () {
        User.logout().success(function () {
            Navigator.changePath('/');
        });
    };

    $scope.getActiveClass = function (pathPrefix) {
        if (pathPrefix.length == 0 && Navigator.prefix == 0 && Navigator.nodePath == 0) {
            return "activeTab";
        } else if (pathPrefix.length > 0 &&
            Navigator.prefix == pathPrefix) {
            return "activeTab";
        } else {
            return "";
        }
    };

    $scope.isContentActive = function () {
        if (Navigator.prefix.length == 0 && Navigator.nodePath.length > 0) {
            return "activeTab";
        } else if (Navigator.prefix.substr(0, 5) == 'index') {
            return "activeTab";
        } else {
            return "";
        }
    };

    $scope.searchSubmit = function () {
        if ($scope.searchString.match(/\S/)) {
            Navigator.changePath('search/' + $scope.searchString);
        }
    };

    $("#searchInput").focus(function() {
            $(".searchBox").addClass("searchActive");
        }).blur(function() {
            $(".searchBox").removeClass("searchActive");
        })

}

FindecoMenuCtrl.$inject = ['$scope', 'User', 'Navigator','Fesettings'];
