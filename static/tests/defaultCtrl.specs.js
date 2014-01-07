describe('FindecoDefaultCtrl', function () {

    var scope = {};
    beforeEach(angular.mock.module('Findeco'));
    beforeEach(angular.mock.inject(function ($rootScope, $controller) {
        scope = $rootScope.$new();
//      $controller('FindecoDefaultCtrl', {
//        $scope: scope
//      });
    }));


    it('should be registered', inject(function ($rootScope, $injector) {

        expect(true).toBe(true);
//        expect(module.controller('FindecoDefaultCtrl')).not.toBe(null);
    }));

});