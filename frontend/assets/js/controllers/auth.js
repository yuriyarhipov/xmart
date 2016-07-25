'use strict';

/* Controllers */

angular.module('app')
    .controller('LoginCtrl', ['$scope', '$rootScope', '$http', '$window', function($scope, $rootScope, $http, $window) {
        $scope.onLogin = function(user){
            $http.post('/api/api-token-auth/', user).success(function(data){
                localStorage.setItem('id_token', data.token);
                $scope.app.user = user.username;
                $window.location.href ='#/app/projects';
            });
        };
    }]).controller('ChangePassCtrl', ['$scope', '$http', '$window', function($scope, $http, $window) {
        $scope.onChangePass = function(old_pass, new_pass){            
            $http.post('/api/change_pass/', {'old_pass': old_pass, 'new_pass': new_pass}).success(function(data){
                localStorage.removeItem("id_token");
                $window.location.href ='#/login';
            });
        };
    }]);
