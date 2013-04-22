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


findecoApp
    .directive('followStar', function( ) {
        return {
            restrict : 'A',
            scope: {
                entity: '=',
                markFunc: '=',
                showIf: '=',
                width: '@',
                height: '@'
            },
            replace: true,
            template: '<a class="follow-star">' +
                        '<img ng-src="static/images/star{{entity.isFollowing}}.png" ' +
                'alt="Follow" title="Folgen" width="{{width}}" height="{{height}}" ' +
                'onmouseover="this.src=\'static/images/star{{entity.isFollowing}}_hover.png\';" ' +
                'onmouseout="this.src=\'static/images/star{{entity.isFollowing}}.png\';" ' +
                '/>' +
                      '</a>',
            link : function (scope, element, attrs) {
                if (scope.entity.isFollowing != 0 &&
                    scope.entity.isFollowing != 1 &&
                    scope.entity.isFollowing != 2) {
                    scope.entity.isFollowing = 0;
                }
                var link = angular.element(element[0]);
                scope.$watch('showIf', function(value){
                    link.css('display', scope.showIf ? '' : 'none');
                });
                link.bind('click', toggle);
                function toggle() {
                    var markType = "follow";
                    if (scope.entity.isFollowing == 2) {markType = "unfollow";}
                    scope.markFunc(scope.entity.path, markType).success(function () {
                        if (markType == 'unfollow') {
                            scope.entity.isFollowing = 0;
                        } else {
                            scope.entity.isFollowing = 2;
                        }
                    });
                }

            }
        }
    })
    .directive('spamMark', function( ) {
        return {
            restrict : 'A',
            scope: {
                entity: '=',
                markFunc: '=',
                showIf: '=',
                width: '@',
                height: '@'
            },
            replace: true,
            template: '<a class="spam-mark">' +
                        '<img ng-src="static/images/spam{{entity.isFlagging}}.png" alt="SpamFlag" title="Als Spam markieren" width="{{width}}" height="{{height}}"/>' +
                      '</a>',
            link : function (scope, element, attrs) {
                if (scope.entity.isFlagging != 0 &&
                    scope.entity.isFlagging != 1 &&
                    scope.entity.isFlagging != 2) {
                    scope.entity.isFlagging = 0;
                }

                var link = angular.element(element[0]);
                scope.$watch('showIf', function(value){
                    link.css('display', scope.showIf ? '' : 'none');
                });
                link.bind('click', toggle);
                function toggle() {
                    var markType = "spam";
                    if (scope.entity.isFlagging == 1) {markType = "notspam";}
                    scope.markFunc(scope.entity.path, markType).success(function () {
                        if (markType == 'notspam') {
                            scope.entity.isFlagging = 0;
                        } else {
                            scope.entity.isFlagging = 1;
                        }
                    });
                }
            }
        }
    })
    .directive('creole', function() {
        return {
            restrict : 'A',
            scope: {
                wikiText : '=',
                updateInterval : '@'
            },
            link : function (scope, element, attrs) {
                if (scope.updateInterval == undefined) {
                    scope.updateInterval = 0;
                }
                scope.lastParseTime = 0;
                scope.lastChangeTime = 0;
                scope.$watch('wikiText', function () {
                    if (scope.updateInterval == 0) {
                        parse()
                    } else {
                        scope.lastChangeTime = new Date().getTime();
                        setTimeout(parse, 1000);
                    }
                });
                function parse() {
                    var now = new Date().getTime();
                    if (now - scope.lastChangeTime > 1000 && now - scope.lastParseTime > scope.updateInterval) {
                        if (scope.wikiText != undefined) {
                            var html = Parser.parse(scope.wikiText, "unusedShortTitle", true);
                            element.html(html);
                            scope.lastParseTime = new Date().getTime();
                        }
                    }
                }
                parse();
            }
        }
    });
