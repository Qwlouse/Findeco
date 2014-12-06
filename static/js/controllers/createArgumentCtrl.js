/****************************************************************************************
 * Copyright (c) 2014  Klaus Greff, Maik Nauheim, Johannes Merkert                      *
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

findecoApp.controller(
    'FindecoCreateArgumentCtrl',
    function ($scope, $routeParams, Backend, Message, Navigator) {
        $scope.getNodePath = function () {
            return Navigator.nodePath;
        };

        $scope.step = 1;
        $scope.heading = "";
        $scope.text = "";

        $scope.nextStep = function () {
            if (($scope.step == 2) && $scope.argumentHasText()) {
                $scope.step++;
            }
        };

        $scope.setStep = function (step) {
            if ((step < $scope.step) && (step > 0)) {
                $scope.step = step;
            }
        };

        $scope.previousStep = function () {
            $scope.step--;
        };

        $scope.argumentHasText = function () {
            return ((angular.isString($scope.heading)) && (angular.isString($scope.text)) &&
                    ($scope.heading.length > 2) && ($scope.text.length > 2));
        };

        $scope.submit = function () {
            var submitData = {
                argument: {
                    heading: $scope.heading,
                    text: $scope.text
                }
            };
            $scope.submitting = true;
            Backend.storeArgument(Navigator.nodePath, submitData).success(function (data) {
                $scope.submitting = undefined;
                if (data.storeArgumentResponse != undefined) {
                    Navigator.changePath(data.storeArgumentResponse.path);
                }
                if (data.errorResponse != undefined) {
                    $scope.error = data.errorResponse;
                }
            }).error(function (response) {
                $scope.submitting = undefined;
                $scope.error = {
                    errorID: "_noConnectionToBackend_",
                    additionalInfo: ""
                };
            });
        };

        $scope.cancelProposal = function () {
            Navigator.changePath(Navigator.nodePath);
        }
    });

