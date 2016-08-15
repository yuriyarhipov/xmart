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
        $scope.checkboxTables = {};
        $scope.onChange = function(){
            $http.get('/api/by_technology/' + $scope.vendor.selected + '/' + $scope.network.selected + '/').success(function(data){
                $scope.tables = data;
                $scope.url_tables = '/api/get_excel/?';
                for (var i in data){
                    $scope.checkboxTables[data[i]] = true;
                }
                $scope.onClicktable();
            });

        };
        $scope.onChange();
        $scope.onClicktable = function(){
          $scope.url_tables = '/api/get_excel/?';
          for (var table_name in $scope.checkboxTables){
              if ($scope.checkboxTables[table_name]){
                  $scope.url_tables += '&table=' + table_name;
              }
          }
        };
    }]);
