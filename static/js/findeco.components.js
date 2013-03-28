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
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

//////////////////// findeco-graph Directive ///////////////////////////////////
/*
 <div follow-star entity="data" markFunc="markNode"/>
 */


findecoApp.directive('followStar', function( ) {
    return {
        restrict : 'A',
        scope: {
            entity: '=',
            markFunc: '=',
            showIf: '='
        },
        replace: true,
        template: '<a class="follow-star">' +
                    '<img src="static/images/star{{entity.isFollowing}}.png" alt=""/>' +
                  '</a>',
        link : function (scope, element, attrs) {

            var link = angular.element(element[0]);
            scope.$watch(scope.showIf, function(value){
                link.css('display', scope.showIf ? '' : 'none');
            });
            link.bind('click', toggle);
            function toggle() {
                console.log('toggle', scope.entity.isFollowing);
                var markType = "follow";
                if (scope.entity.isFollowing == 2) {markType = "unfollow";}
                scope.markFunc(scope.entity.path, markType).success(function () {

                    if (scope.entity.isFollowing == 2) {
                        scope.entity.isFollowing = 0;
                    } else {
                        scope.entity.isFollowing = 2;
                    }
                });
            }

        }
    }
});
