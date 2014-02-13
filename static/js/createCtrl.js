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

function FindecoCreateCtrl($scope, $routeParams, Backend, TMP, Message, Navigator) {
    $scope.settings = {
        type: $routeParams.type
    };

    $scope.radioModel = '';
    $scope.initialAlternative = '';

    $scope.showIf = function (matchArray) {
        for (var m in matchArray) {
            if (matchArray[m] == $scope.settings.type) {
                return true;
            }
        }
        return false;
    };

    $scope.checkWikiCompatibility = function (text) {
        if (text == undefined
            || text == '') {
            return 'Empty';
        }
        Parser.parse(text);
        if (Parser.isErrorState()) {
            return 'ParseError';
        }

        return true;
    };

    $scope.getButtonState = function () {
        if ($scope.blockButton == true) {
            return "btn btn-primary active";
        } else {
            return "btn btn-primary inActive";
        }
    };

    $scope.getFormLockState = function () {
        return $scope.blockButton;
    };

    $scope.submit = function () {
        if ($scope.blockButton == true) {
            return;
        }
        //Check that both fields are modified
        if (Message.localize('_editFieldPretext_') == $scope.tmp.text) {
            Message.send('error', '_createNotChanged_');
            return;
        }

        if (( $scope.initialAlternative == $scope.tmp.textAlternative ) &&
            ( $scope.tmp.textAlternative != "")) {
            Message.send('error', '_alternativeNotChanged_');
            return;
        }

        //Check that the heading was modified
        var h1Regex = new RegExp('^[^=]*=([a-zA-ZÜÖÄüöäß0-9 -_,:;§@]+)=[^=]');
        var pretextMatches = Message.localize('_editFieldPretext_').match(h1Regex);
        var inputMatches = $scope.tmp.text.match(h1Regex);
        if ((pretextMatches.length > 1) && (inputMatches.length > 1) &&
            (pretextMatches[1].length > 0) &&
            ((pretextMatches[1] == inputMatches[1]) || (inputMatches[1].length == 0))) {
            Message.send('error', '_createHeadingNotChanged_');
            return;
        }

        var params = {};
        var test = false;
        switch ($scope.settings.type) {
            case 'argument':
                test = $scope.checkWikiCompatibility($scope.tmp.text);
                if (test != true) {
                    Message.send('error', '_argumentText' + test + '_');
                    break;
                }
                // Past watchdog

                params['argumentType'] = 'neut';
                params['wikiText'] = $scope.tmp.text;
                break;
            case 'topic':
                test = $scope.checkWikiCompatibility($scope.tmp.text);
                if (test != true) {
                    Message.send('error', '_text' + test + '_');
                    break;
                }
                // Past watchdog

                params['wikiText'] = $scope.tmp.text;
                break;
            case 'derivate':
                if ($scope.tmp.argumentType != 'con' && $scope.tmp.argumentType != 'neut') {
                    Message.send('error', '_derivateArgumentMissing_');
                    break;
                }
                test = $scope.checkWikiCompatibility($scope.tmp.text);
                if (test != true) {
                    Message.send('error', '_derivateText' + test + '_');
                    break;
                }
                test = $scope.checkWikiCompatibility($scope.tmp.textAlternative);
                if (test != true) {
                    Message.send('error', '_derivateTextAlternative' + test + '_');
                    break;
                }
                // Past watchdog

                params['argumentType'] = $scope.tmp.argumentType;
                params['wikiText'] = $scope.tmp.text;
                params['wikiTextAlternative'] = $scope.tmp.textAlternative;
                break;
            case 'opposing':
                test = $scope.checkWikiCompatibility($scope.tmp.textAlternative);
                if (test != true) {
                    Message.send('error', '_opposingTextAlternative' + test + '_');
                    break;
                }
                // Past watchdog

                params['wikiTextAlternative'] = $scope.tmp.textAlternative;
                break;
        }

        if (angular.equals(params, {})) {
            return;
        }
        $scope.blockButton = true;
        Backend.storeText(Navigator.nodePath, params)
            .success(function (data) {
                if (data.storeTextResponse != undefined) {
                    $scope.tmp.text = '';
                    $scope.tmp.textAlternative = '';
                    $scope.tmp.argumentType = '';
                    Navigator.changePath(data.storeTextResponse.path);
                }
                if (data.errorResponse != undefined) {
                    Message.send('error', data.errorResponse.errorMessage);
                }
                $scope.blockButton = false;

            })
            .error(function (data) {
                $scope.blockButton = false;
            });
    };

    $scope.cancel = function () {
        history.back();
    };

    $scope.tmp = TMP;

    $scope.tmp.text = "";
    $scope.tmp.textAlternative = "";
    if (!($scope.settings.type == 'opposing')) {
        $scope.tmp.text = Message.localize('_editFieldPretext_');
    }
    if (($scope.settings.type == 'derivate') || ($scope.settings.type == 'opposing')) {
        $scope.tmp.textAlternative = Message.localize('_editFieldPretext_');
    }

    if ($scope.settings.type == 'derivate') {
        var paragraphs = [];
        var wikiText = "";
        $scope.blockButton = true;
        Backend.loadText(paragraphs, Navigator.nodePath).success(function () {
            $scope.blockButton = false;
            for (var i = 0; i < paragraphs.length; i++) {
                var tmpText = paragraphs[i]['wikiText'];
                tmpText = tmpText.replace(/={2}[ ]\[{2}.*\|/, "= ");
                wikiText += tmpText.replace(/]{2}[ ]={2}/, " =") + "\n\n\n";
            }
            $scope.tmp.textAlternative = wikiText;
            $scope.initialAlternative = wikiText;
        });
    }

    if ($scope.settings.type == 'argument') {
        $scope.tmp.argumentType = 'neut';
    }
}

FindecoCreateCtrl.$inject = ['$scope', '$routeParams', 'Backend', 'TMP', 'Message', 'Navigator'];