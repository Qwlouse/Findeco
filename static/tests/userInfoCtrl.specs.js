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

describe('FindecoUserInfoCtrl', function() {
    var scope = {};
    var ctrl = null;
    var promiseMock = {
        success: function (f) {return this;},
        error: function (f) {return this;},
        then: function (f, g, h) {return this;},
        catch: function (f) {return this;},
        finally: function (f) {return this;}
    };


    beforeEach( function(){
        angular.mock.module('Findeco');
        angular.mock.inject(function ($rootScope, $controller) {
            var Backend = {
                loadUserInfo: function(name) {
                    return promiseMock;
                }
            };
            scope = $rootScope.$new();
            ctrl = $controller('FindecoUserInfoCtrl', {
                $scope: scope,
                $routeParams: {name:'herbert'},
                Backend: Backend
            });
        });
    });



    it('should be registered', inject(function () {
        expect(ctrl).not.toBe(null);
    }));
});