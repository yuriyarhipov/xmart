'use strict';

/* Controllers */

angular.module('app')
    .controller('byTechnologyCtrl', ['$scope', '$http', function($scope, $http) {
        $scope.vendors = ['Ericsson', 'Nokia', 'Huawei', ];
        $scope.vendor = {
            'selected': 'Ericsson'
        }
        $scope.networks = ['GSM', 'WCDMA', 'LTE'];
        $scope.network = {
            'selected': 'GSM'
        };
        $scope.onChange = function(){
            $http.get('/api/by_technology/' + $scope.vendor.selected + '/' + $scope.network.selected + '/').success(function(data){
                $scope.tables = data;
            });
        };
        $scope.onChange();
    }]);
