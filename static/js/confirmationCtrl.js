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

function FindecoConfirmationCtrl($scope, User, $routeParams, Navigator) {
    $scope.user = User;
    $scope.activationKey = $routeParams.param.replace('/', '');
    $scope.manualEntry = $scope.activationKey.length == 0;
    console.log($scope.activationKey);
    if (Navigator.prefix == "activate") {
        $scope.title = "_accountActivationFormTitle_";
        $scope.text = "_accountActivationText_";
        $scope.submitButton = "_accountActivateBtn_";
    } else if (Navigator.prefix == "confirm") {
        $scope.title = "_accountConfirmFormTitle_";
        $scope.text = "_accountConfirmText_";
        $scope.submitButton = "_accountRecoverBtn_";
    } else if (Navigator.prefix == "confirm_email") {
        $scope.title = "_accountConfirmEmailFormTitle_";
        $scope.text = "_accountConfirmEmailText_";
        $scope.submitButton = "_accountConfirmEmailBtn_";
    }

    $scope.activate = function () {
        if (Navigator.prefix == "activate") {
            User.activate($scope.activationKey).success(function () {
                $scope.text = "_accountActivationFinished_";
            }).error(function () {
                $scope.manualEntry = true;
            });

        } else if (Navigator.prefix == "confirm") {
            User.confirm($scope.activationKey).success(function () {
                $scope.text = "_accountRecoveryConfirmed_";
            }).error(function () {
                $scope.manualEntry = true;
            });
        } else if (Navigator.prefix == "confirm_email") {
            User.confirmEmail($scope.activationKey).success(function () {
                $scope.text = "_accountEmailConfirmed_";
            }).error(function () {
                $scope.manualEntry = true;
            });
        }
    };

    if (!$scope.manualEntry) {
        $scope.activate();
    }
}

FindecoConfirmationCtrl.$inject = ['$scope', 'User', '$routeParams' , 'Navigator'];
