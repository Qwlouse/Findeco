describe('FindecoDefaultCtrl', function () {

    var scope = {};
    var ctrl = null;

    beforeEach( function(){
        angular.mock.module('Findeco');
        angular.mock.inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            ctrl = $controller('FindecoDefaultCtrl', {
                $scope: scope,
                Fesettings: {}
            });
        });
    });



    it('should be registered', inject(function ($rootScope, $injector) {
        expect(ctrl).not.toBe(null);
    }));

});