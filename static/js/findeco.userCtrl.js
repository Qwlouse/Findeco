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

function FindecoUserCtrl($scope, $location, User, $routeParams, Message) {
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
    	Message.send("error", "_textCreateSendBtn_");
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
    		
    		Message.send("error", "_textCreateSendBtn_");
    		console.log("DPR not checked");
    		return "";
    	}
    	Message.send("error", "foo");
    	User.register($scope.username, $scope.password, $scope.mail).success(function () {
            $location.path('/');
        });
    };
    
    $scope.activate = function() {
    	 //$scope.alerts.push({type: 'success', msg: "Bitte Emails checken"});
    	//Message.send("error", "foo");
    //	$scope.accountActivationKey = $routeParams.accountActivationKey
    	//accountActivationKey
    	if(!($location.path().substr(1, 8) == "activate")){
    		return "";
    	}
    	// /activate/
    	User.activate($routeParams.param).success(function () {
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

    $scope.searchSubmit = function() {
        $location.path('search/'+$scope.searchString);
    };

    $scope.storeUserSettings = function() {
        User.storeSettings();
    };

    $scope.parse = function (text) {
        if ( text != undefined && text.length > 0 )
            return Parser.parse(text, null, true);
        return "";
    };

    $scope.activate();
   
}

FindecoUserCtrl.$inject = ['$scope', '$location', 'User', '$routeParams' , 'Message'];
