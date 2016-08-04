'use strict';

/* Controllers */

angular.module('app')
    .controller('tableCtrl', ['$scope', '$http', '$stateParams', function($scope, $http, $stateParams) {
        var columns = [];
        $scope.table = $stateParams.table;
        $scope.table_config = {
            columnDefs: columns,
            enableGridMenu: true,
            enableSelectAll: true,
            enableFiltering: true,
            flatEntityAccess: true,
            showGridFooter: true,
        };
        $http.get('/api/table/' + $stateParams.table + '/').success(function(data) {
            for (var col_id in data.columns){
                columns.push({
                    field: data.columns[col_id],
                    name: data.columns[col_id],
                    width:100
                })
            }
            $scope.table_config.data = data.data;

        });

    }]);
