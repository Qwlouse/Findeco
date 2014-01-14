

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

    it('should have a login function', function () {
        expect(angular.isFunction(userService.login)).toBe(true);
    });

    it('should set the userInfo details after successful login', function () {
        //set up some data for the http call to return and test later.

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