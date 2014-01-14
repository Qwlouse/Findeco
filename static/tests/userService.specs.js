

describe('FindecoUserService', function () {
    var userService, httpBackend;

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
        expect(userService.isLoggedIn).toBe(false);
    });

    it('should have a login function', function () {
        expect(angular.isFunction(userService.login)).toBe(true);
    });

    it('should set the userInfo details after succesful login', function () {
        //set up some data for the http call to return and test later.
        var returnData = {
            loginResponse: {
                userInfo: {
                    displayName: 'hugo',
                    description: 'beschreibung'
                },
                userSettings: {
                    rsskey: 'abcdefg',
                    email: 'hugo@abc.de',
                    followees: []
                }
            }
        };
        // flush the initial loadUserSettings
        httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
        httpBackend.flush();

        httpBackend.expectPOST('/.json_login/').respond(returnData);

        //create an object with a function to spy on.
        var test = {
          handler: function() {}
        };
        spyOn(test, 'handler');

        //make the call.
        userService.login('hugo', '1234').then(test.handler);
        httpBackend.flush();

        expect(test.handler).toHaveBeenCalled();
        expect(userService.isLoggedIn).toBe(true);
        expect(userService.displayName).toBe('hugo');
        expect(userService.description).toBe('beschreibung');
        expect(userService.rsskey).toBe('abcdefg');
        expect(userService.email).toBe('hugo@abc.de');
        expect(userService.followees).toBe([]);
    });

    it('should have a logout function', function () {
        expect(angular.isFunction(userService.logout)).toBe(true);
    });
});