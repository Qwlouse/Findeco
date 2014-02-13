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

describe('FindecoUserCtrl', function() {
    var scope = {};
    var ctrl = null;
    var loginPromise = new PromiseMock();
    var UserServiceMock = {
        displayName: 'hugo',
        login: function() {
            return loginPromise;
        }
    };

    beforeEach(function() {
        angular.mock.module('Findeco');
        angular.mock.inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            ctrl = $controller('FindecoUserCtrl', {
                $scope: scope,
                Backend: {},
                Message: {},
                User: UserServiceMock
            });
            spyOn(UserServiceMock, 'login').andReturn(loginPromise);
        });
    });
    it('should be registered', inject(function () {
        expect(ctrl).not.toBe(null);
    }));

    it('should expose the UserService as scope.user', function() {
        expect(scope.user).toBe(UserServiceMock);
    });

    it('should provide some fields on scope', function() {
        expect(scope.displayNameTmp).toBeDefined();
        expect(scope.username).toBeDefined();
        expect(scope.password).toBeDefined();
        expect(scope.password2).toBeDefined();
        expect(scope.mail).toBeDefined();
        expect(scope.TOS).toBeDefined();
        expect(scope.DPR).toBeDefined();
    });

    describe('the login function', function() {
        it('should call UserService.login with parameters from scope', function(){
            scope.username = 'herbert';
            scope.password = '00000000';

            scope.login();
            expect(UserServiceMock.login).toHaveBeenCalledWith(scope.username, scope.password);
        });
    });

});