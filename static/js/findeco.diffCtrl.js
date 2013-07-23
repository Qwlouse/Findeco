/****************************************************************************************
 * Copyright (c) 2013 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
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

function FindecoDiffCtrl($scope, Backend, Navigator) {
	
    $scope.nav = Navigator;
    $scope.path1 = Navigator.nodePath;
    $scope.path2 = Navigator.segments.compare;
    $scope.text1Loaded = false;
    $scope.text2Loaded = false;
    $scope.diffIsLoading = true;
    $scope.changes = [];
    $scope.loadTexts = function (path1, path2) {
        $scope.text1 = "";
        $scope.text2 = "";
        var text1Paragraphs = [];
        Backend.loadText(text1Paragraphs, path1).success(function (d) {
            $scope.text1Loaded = true;
            for (var i = 0; i < text1Paragraphs.length; i++) {
                $scope.text1 += text1Paragraphs[i].wikiText;
            }
            $scope.createDiff();
        });
        var text2Paragraphs = [];
        Backend.loadText(text2Paragraphs, path2).success(function (d) {
            $scope.text2Loaded = true;
            for (var i = 0; i < text2Paragraphs.length; i++) {
                $scope.text2 += text2Paragraphs[i].wikiText;
            }
            $scope.createDiff();
        });
    };

    $scope.createDiff = function () {
        if ($scope.text1Loaded && $scope.text2Loaded) {
            console.log("creating Diff");
            $scope.changes = JsDiff.diffWords($scope.text1, $scope.text2);
            $scope.diffIsLoading =false;
        }
    };
    $scope.isLoading = function (){
    	return $scope.diffIsLoading;
    };
    $scope.loadTexts($scope.path1, $scope.path2);
}

FindecoDiffCtrl.$inject = ['$scope', 'Backend', 'Navigator'];
