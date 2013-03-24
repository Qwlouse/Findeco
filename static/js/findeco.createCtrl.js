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

function FindecoCreateCtrl($scope, $location, Backend, TMP, Message) {
    $scope.radioModel = '';

    $scope.relocate = function (target) {
        $location.path(target + '/' + THELocatoooooooor.getSanitizedArgumentFreePath());
    }

    $scope.parse = function (text) {
        if ( text != undefined && text.length > 0 )
            return Parser.parse(text, null, true);
        return "";
    };

    $scope.submit = function (type) {
        //TODO: input validation
        var params = {};
        if ( type == 'argument' ) {
            params['wikiText'] = $scope.tmp.text;
            params['argumentType'] = $scope.tmp.argumentType;
        }
        if ( type == 'alternative' ) {
            params['wikiText'] = $scope.tmp.text;
            params['wikiTextAlternative'] = $scope.tmp.textAlternative;
            params['argumentType'] = $scope.tmp.argumentType;
        }
        if ( type == 'new' ) {
            params['wikiText'] = $scope.tmp.text;
        }
        Backend.storeText(THELocatoooooooor.getSanitizedArgumentFreePath(),params)
            .success(function (data) {
                if ( data.storeTextResponse != undefined ) {
                    $scope.tmp.text = '';
                    $scope.tmp.textAlternative = '';
                    $scope.tmp.argumentType = '';

                    $location.path(data.storeTextResponse.path);
                }
                if ( data.errorResponse != undefined ) {
                    Message.send('error',data.errorResponse.errorMessage);
                }
            });
    }

    $scope.tmp = TMP;
}

FindecoCreateCtrl.$inject = ['$scope', '$location', 'Backend', 'TMP', 'Message'];