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

function FindecoArgumentCtrl($scope, Backend, User, TMP, Navigator) {
    $scope.nav = Navigator;
    $scope.tmp = TMP;
    $scope.user = User;

    $scope.markNode = Backend.markNode;

    $scope.argumentList = [];
    
    $scope.isLoading = function (){
    	return $scope.argumentIsLoading ;
    };

    $scope.createArgumentSlug = function (text) {
        var stringAddition = "";
        if (text.length > 140) {
            stringAddition = " ...";
        }
        return text.substr(0, 140) + stringAddition;
    };
    
    function amendArguments() {
        for (var i = 0; i < $scope.argumentList.length; ++i) {
            var arg = $scope.argumentList[i];
            arg.path = $scope.nav.getPathForArgument(arg.argType, arg.index);
            console.log(arg);
        }
        $scope.argumentIsLoading  = false;
    }

    $scope.updateArgumentList = function () {
    	$scope.argumentIsLoading = true;
        Backend.loadArgument($scope.argumentList , $scope.nav.nodePath).success(amendArguments);
    };

    $scope.updateArgumentList();
}

FindecoArgumentCtrl.$inject = ['$scope', 'Backend', 'User', 'TMP', 'Navigator'];