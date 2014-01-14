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
    }));

    it('should have get getActiveClass function', inject(function () {
        expect(angular.isFunction(scope.getActiveClass)).toBe(true);
    }));


    it('should have a logout function', inject(function () {
        expect(angular.isFunction(scope.logout)).toBe(true);
    }));

});
