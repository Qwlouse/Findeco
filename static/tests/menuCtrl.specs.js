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

describe('FindecoMenuCtrl', function(){
    var scope = {};
    var ctrl = null;

    beforeEach(angular.mock.module('Findeco'));

    beforeEach(angular.mock.inject(function ($rootScope, $controller) {
        scope = $rootScope.$new();
        ctrl = $controller('FindecoMenuCtrl', {
            $scope: scope,
            Fesettings: {}
        });
    }));

    it('should be registered', inject(function ($rootScope, $injector) {
        expect(ctrl).not.toBe(null);
        expect(scope.user).not.toBe(null);
        expect(scope.fesettings).not.toBe(null);
    }));

    it('should have a getActiveClass function', inject(function () {
        expect(angular.isFunction(scope.getActiveClass)).toBe(true);
    }));

    describe('Logout', function (){
        it('should have a logout function', inject(function () {
            expect(angular.isFunction(scope.logout)).toBe(true);
        }));

        it('expect logout function to be called', inject(function () {
            spyOn(scope, 'logout');
            scope.logout();
            expect(scope.logout).toHaveBeenCalled();
        }));
    });

    it('should have a searchSubmit function', inject(function(){
        expect(angular.isFunction(scope.searchSubmit)).toBe(true);
    }));
});
