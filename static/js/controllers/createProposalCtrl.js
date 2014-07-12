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

findecoApp.controller('FindecoCreateProposalCtrl', function ($scope, $routeParams, Backend, Message, Navigator, TMP) {
    $scope.step = 1;
    $scope.setProposalType = function (type) {
        $scope.proposalType = type;
        $scope.step++;
    };
    $scope.nextStep = function () {
        $scope.step++;
        if (($scope.step == 3) && ($scope.proposalType != 'refinement')) {
            $scope.step++;
        }
    };
    $scope.previousStep = function () {
        $scope.step--;
        if (($scope.step == 3) && ($scope.proposalType != 'refinement')) {
            $scope.step--;
        }
    };
    $scope.submit = function () {
        alert({{"_proposalSubmittedAlert_"|i18n}});
    };
});

