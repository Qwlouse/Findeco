

describe('FindecoUserService', function () {
    var userService;

    //excuted before each "it" is run.
    beforeEach(function (){

      //load the module.
      angular.mock.module('FindecoUserService');

      //inject your service for testing.
      angular.mock.inject(function(User) {
        userService = User;
      });
    });

    //check to see if it has the expected function
    it('should have an exciteText function', function () {
        expect(angular.isFunction(userService.login)).toBe(true);
    });
});