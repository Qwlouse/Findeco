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

findecoApp.controller('FindecoConfirmationCtrl', function ($scope, $routeParams, Navigator, User) {
    $scope.user = User;
    $scope.activationKey = $routeParams.param != undefined ? $routeParams.param.replace('/', '') : '';
    $scope.completed = $scope.activationKey.length > 0;
    $scope.error = false;

    if (Navigator.type == "activate") {
        $scope.title = "_accountActivationFormTitle_";
        $scope.text = "_accountActivationText_";
        $scope.submitButton = "_accountActivateBtn_";
    } else if (Navigator.type == "confirm") {
        $scope.title = "_accountConfirmFormTitle_";
        $scope.text = "_accountConfirmText_";
        $scope.submitButton = "_accountRecoverBtn_";
    } else if (Navigator.type == "confirm_email") {
        $scope.title = "_accountConfirmEmailFormTitle_";
        $scope.text = "_accountConfirmEmailText_";
        $scope.submitButton = "_accountConfirmEmailBtn_";
    }

    $scope.activate = function () {
        $scope.error = false;
        if (Navigator.type == "activate") {
            User.activate($scope.activationKey).success(function () {
                $scope.text = "_accountActivationFinished_";
                $scope.completed = true;
            }).error(function (d) {
                $scope.error = d.errorResponse;
                $scope.completed = false;
            });

        } else if (Navigator.type == "confirm") {
            User.confirm($scope.activationKey).success(function () {
                $scope.text = "_accountRecoveryConfirmed_";
                $scope.completed = true;
            }).error(function (d) {
                $scope.error = d.errorResponse;
                $scope.completed = false;
            });
        } else if (Navigator.type == "confirm_email") {
            User.confirmEmail($scope.activationKey).success(function () {
                $scope.text = "_accountEmailConfirmed_";
                $scope.completed = true;
            }).error(function (d) {
                $scope.error = d.errorResponse;
                $scope.completed = false;
            });
        }
    };

    if ($scope.completed) {
        $scope.activate();
    }
});
