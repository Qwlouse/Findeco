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

describe('FindecoUserService', function () {
    var userService, httpBackend;
    var userInfo = {
        displayName: 'hugo',
        description: 'beschreibung'
    };

    var userSettings = {
        rsskey: 'abcdefg',
        email: 'hugo@abc.de',
        followees: []
    };

    var loginResponse = {
        loginResponse: {
            userInfo: userInfo,
            userSettings: userSettings
        }
    };

    var loadUserSettingsResponse = {
        loadUserSettingsResponse: {
            userInfo: userInfo,
            userSettings: userSettings
        }
    };

    var logoutResponse = {
        logoutResponse: {}
    };

    //excuted before each "it" is run.
    beforeEach(function (){

      //load the module.
      angular.mock.module('FindecoUserService');

      //inject your service for testing.
      angular.mock.inject(function($httpBackend, User) {
          userService = User;
          httpBackend = $httpBackend
      });
    });

    ///////////////// Initialization ///////////////////////////////////////////

    it('should initialize with a .json_loadUserSettings call', function () {
        httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
        httpBackend.flush();
    });

    it('should initialize user if loadUserSettings succeeds', function () {
        httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
        httpBackend.flush();
        expect(userService.isLoggedIn).toBe(true);
        expect(userService.displayName).toBe(userInfo.displayName);
        expect(userService.description).toBe(userInfo.description);
        expect(userService.rsskey).toBe(userSettings.rsskey);
        expect(userService.email).toBe(userSettings.email);
        expect(userService.followees).toEqual(userSettings.followees);
    });

    it('should have empty user details if loadUserSettings does not succeed', function () {
        httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
        httpBackend.flush();
        expect(userService.isLoggedIn).toBe(false);
        expect(userService.displayName).toBe('');
        expect(userService.description).toBe('');
        expect(userService.rsskey).toBe('');
        expect(userService.email).toBe('');
        expect(userService.followees).toEqual([]);
    });

    ///////////////// Login ////////////////////////////////////////////////////

    it('should have a login function', function () {
        expect(angular.isFunction(userService.login)).toBe(true);
    });

    it('should set the userInfo details after successful login', function () {
        // flush the initial loadUserSettings
        httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
        httpBackend.flush();

        httpBackend.expectPOST('/.json_login/').respond(loginResponse);
        //make the call.
        userService.login('hugo', '1234');
        httpBackend.flush();

        expect(userService.isLoggedIn).toBe(true);
        expect(userService.displayName).toBe(userInfo.displayName);
        expect(userService.description).toBe(userInfo.description);
        expect(userService.rsskey).toBe(userSettings.rsskey);
        expect(userService.email).toBe(userSettings.email);
        expect(userService.followees).toEqual(userSettings.followees);
    });

    ///////////////// Logout ///////////////////////////////////////////////////

    it('should have a logout function', function () {
        expect(angular.isFunction(userService.logout)).toBe(true);
    });

    it('should remove the user details after successful logout', function () {
        httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
        httpBackend.flush();
        httpBackend.expectGET('/.json_logout/').respond(logoutResponse);
        userService.logout();
        httpBackend.flush();
        expect(userService.isLoggedIn).toBe(false);
        expect(userService.displayName).toBe('');
        expect(userService.description).toBe('');
        expect(userService.rsskey).toBe('');
        expect(userService.email).toBe('');
        expect(userService.followees).toEqual([]);
    });
});