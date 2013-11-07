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

function FindecoHelpCtrl($scope) {
    // todo: Is this used at all?
    // todo: Yes Now it is!!!!! Finally!!!
    $scope.visible=true;

    $scope.hide =function(){
        $scope.visible=false;
    }

    $scope.$on('change_Help', function(e,num) {
            $scope.visible=true;


            if (num==1){
                $scope.helptext ="Helptext ID" +num;
            }
            if (num==2){
                $scope.helptext ="Helptext ID" +num;
            }


                $scope.$apply();

    });


}

FindecoHelpCtrl.$inject = ['$scope',  'Help'];