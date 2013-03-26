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

function FindecoUserCtrl($scope, $location, User) {
    $scope.user = User;

    $scope.login = function () {
        User.login($scope.username, $scope.password).success(function () {
            $location.path('/');
        });
    };

    $scope.logout = function() {
        User.logout().success(function() {
            $location.path('/');
        });
    };
    
    $scope.register = function() {
    	console.log($scope.TOS)
    	if (($scope.password == undefined) || ($scope.mail ==  undefined) || ($scope.username ==  undefined)) {
    		console.log("Missing Fields");
    		return "";
    	}
    	if ($scope.password != $scope.password2) {
    		console.log("Not matching Passwords");
    		return "";
    	}
    	
    	if ($scope.TOS != true) {
    		console.log("TOS not checked");
    		return "";
    	}
    	if ($scope.DPR != true) {
    		console.log("DPR not checked");
    		return "";
    	}
     	
    	User.register($scope.username, $scope.password, $scope.mail).success(function () {
            $location.path('/');
        });
    };

    $scope.getActiveClass = function(path) {
        if ($location.path().substr(0, path.length) == path) {
            return "activeTab";
        } else {
            return "";
        }
    };

    $scope.storeUserSettings = function() {
        User.storeSettings();
    };
}

FindecoUserCtrl.$inject = ['$scope', '$location', 'User'];