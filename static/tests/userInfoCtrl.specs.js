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
        success_func: null,
        error_func: null,

        success: function (f) {
            this.success_func = f;
            return this;
        },
        error: function (f) {
            this.error_func = f;
            return this;
        },
        then: function (f, g, h) {
            this.success_func = f;
            this.error_func = g;
            return this;
        },
        catch: function (f) {return this;},
        finally: function (f) {return this;}
    };
    var UserServiceMock = {
        display_name: 'Simon',
        isLoggedIn: true,
        isFollowing: function () {
            return true;
        }
    };
    var Backend = {
        loadUserInfo: function(name) {
            return promiseMock;
        }
    };
    spyOn(Backend, 'loadUserInfo').andReturn(promiseMock);



    beforeEach(function() {
        angular.mock.module('Findeco');
        angular.mock.inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            ctrl = $controller('FindecoUserInfoCtrl', {
                $scope: scope,
                $routeParams: {name:'herbert/'},
                Backend: Backend,
                User: UserServiceMock
            });
        });
    });

    it('should be registered', inject(function () {
        expect(ctrl).not.toBe(null);
    }));

    it('should expose the UserService as scope.user', function() {
        expect(scope.user).toBe(UserServiceMock);
    });

    it('should provide a displayUser object', function() {
        expect(scope.displayUser).toBeDefined();
        expect(scope.displayUser.name).toBe('herbert');
        expect(scope.displayUser.description).toBe('');
        expect(scope.displayUser.isFollowing).toBeFalsy();
        expect(scope.displayUser.exists).toBeFalsy();
    });

    it('should call the Backend.loadUserInfo function', function() {
        expect(Backend.loadUserInfo.toHaveBeenCalled);
    });

    it('on success of Backend.loadUserInfo it should update the displayUser', function() {
        expect(Backend.loadUserInfo.toHaveBeenCalled);
        expect(promiseMock.success_func).not.toBeNull();
        promiseMock.success_func({
                loadUserInfoResponse: {
                    userInfo: {
                        displayName:'Herbert',
                        description:'not herbert'
                    }}});
        expect(scope.displayUser.name).toBe('Herbert');
        expect(scope.displayUser.description).toBe('not herbert');
        expect(scope.displayUser.exists).toBeTruthy();
    });


});