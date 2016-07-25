'use strict';

/* Controllers */

angular.module('app')
    .controller('ProjectsCtrl', ['$scope', '$http', function($scope, $http) {
        $http.get('/api/projects').success(function(data) {
            $scope.projects = data;
        });
    }])
    .controller('CreateProjectCtrl', ['$scope', '$http', '$window', function($scope, $http, $window) {
        $scope.onSave = function(data){
            $http.post('/api/projects/', {'name': data}).success(function(data) {
                $window.location.href ='#/app/projects';
            });
        }
    }]);
