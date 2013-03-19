
function FindecoMenuCtrl($scope, $location, FindecoService, FindecoUserService) {
    $scope.isLoggedIn = FindecoUserService.isLoggedIn();
    $scope.login = function () {

        FindecoService.post({action: '.json_login/', 'username': $scope.username, 'password': $scope.password}, function(data) {
            FindecoUserService.set(data);
            $location.path('/');
        });
    };
}