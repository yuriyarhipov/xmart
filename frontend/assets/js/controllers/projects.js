'use strict';

/* Controllers */

angular.module('app')
    .controller('ProjectsCtrl', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {
        var get_projects = function(){
            $http.get('/api/projects').success(function(data) {
                $scope.projects = data;
            });
        };
        get_projects();
        $scope.onDelete = function(id){
            $http.delete('/api/projects/' + id + '/').success(function(){
                get_projects();
            });
        }
        $scope.onClick = function(id){
            $cookies.put('id_project', id);            
        };
    }])
    .controller('CreateProjectCtrl', ['$scope', '$http', '$window', function($scope, $http, $window) {
        $scope.onSave = function(data){
            $http.post('/api/projects/', {'name': data}).success(function(data) {
                $window.location.href ='#/app/projects';
            });
        }
    }]);
