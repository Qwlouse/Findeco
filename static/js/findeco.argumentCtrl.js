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

function FindecoArgumentCtrl($scope, $location, $routeParams, Backend, User, TMP) {
    $scope.tmp = TMP;
    $scope.user = User;

    $scope.path = THELocatoooooooor.getSanitizedArgumentFreePath();
    $scope.argumentPath = THELocatoooooooor.getSanitizedPath();

    $scope.isTextLoaded = false;
    $scope.paragraphList = [];
    $scope.argumentList = [];

    $scope.getPath = function () {
        return THELocatoooooooor.getSanitizedArgumentFreePath();
    };

    $scope.parse = function(text,shortTitle) {
        return Parser.parse(text,shortTitle,true);
    };

    $scope.relocateRelativeTo = function(shortTitle,index) {
        var path = $scope.path;
        if ( $scope.path == '/' ) {
            path = '';
        }
        $location.path(THELocatoooooooor.getSanitizedPath(shortTitle + '.' + index));
    };

    $scope.updateParagraphList = function() {

    };

    $scope.updateArgument = function () {
        Backend.loadText($scope.paragraphList, $scope.argumentPath).success( function () {
            $scope.isTextLoaded = true;
        });
    };

    $scope.updateArgumentList = function () {
        Backend.loadArgument($scope.argumentList , $scope.path);
    };

    $scope.updateArgumentList();
    if ( THELocatoooooooor.isArgumentPath() ) {
        $scope.updateArgument();
    }
}

FindecoArgumentCtrl.$inject = ['$scope', '$location', '$routeParams', 'Backend', 'User', 'TMP'];