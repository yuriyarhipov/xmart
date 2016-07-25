'use strict';

/* Controllers */

angular.module('app')
    .controller('FilesHubCtrl', ['$scope', '$http', function($scope, $http) {
        $scope.vendors = ['Ericsson', 'Nokia', 'Huawei', 'Universal'];
        $scope.vendor = {
            'selected': 'Ericsson'
        }
        $scope.networks = ['GSM', 'WCDMA', 'LTE'];
        $scope.network = {
            'selected': 'GSM'
        };

        $scope.filetypes = [
            'GSM BSS CNA  OSS FILE',
            'GSM NCS OSS FILE',
            'GSM MRR OSS FILE',
            'Drive Test',
        ];

        $scope.filetype = {
            'selected': 'GSM BSS CNA  OSS FILE'
        }

        $scope.onChangeVendor = function(vendor) {
            $scope.onChangeNetwork()
        };

        $scope.onChangeNetwork = function() {
            if (($scope.network.selected == 'WCDMA') && ($scope.vendor.selected == 'Ericsson')) {
                $scope.filetypes = [
                    'WCDMA RADIO OSS BULK CM XML FILE',
                    'WCDMA TRANSPORT OSS BULK CM XML FILE',
                    'WCDMA Radio and Transport Bulk',
                    'WNCS OSS FILE',
                    'WMRR OSS FILE',
                    'WCDMA LICENSE FILE OSS XML',
                    'WCDMA HARDWARE FILE OSS XML',
                    'HISTOGRAM FORMAT COUNTER',
                    'HISTOGRAM FILE COUNTER - Access Distance',
                    'Drive Test',
                ];
            }
            if (($scope.network.selected == 'WCDMA') && ($scope.vendor.selected == 'Nokia')) {
                $scope.filetypes = [
                    'Configuration Management XML File',
                ];
            }
            if (($scope.network.selected == 'WCDMA') && ($scope.vendor.selected == 'Huawei')) {
                $scope.filetypes = [
                    'MMLCFG',
                    'MML script file',
                ];
            }
            if (($scope.network.selected == 'GSM') && ($scope.vendor.selected == 'Ericsson')) {
                $scope.filetypes = [
                    'GSM BSS CNA  OSS FILE',
                    'GSM NCS OSS FILE',
                    'GSM MRR OSS FILE',
                    'Drive Test',
                ];
            }
            if (($scope.network.selected == 'LTE') && ($scope.vendor.selected == 'Ericsson')) {
                $scope.filetypes = [
                    'LTE RADIO eNodeB BULK CM XML FILE',
                    'LTE TRANSPORT eNodeB BULK CM XML FILE',
                    'LTE LICENSE FILE OSS XML',
                    'LTE HARDWARE FILE OSS XML',
                    'Drive Test',

                ];
            }
            if ($scope.vendor.selected == 'Universal') {
                $scope.filetypes = [
                    'RND',
                ];
            }

            $scope.filetype = {
                'selected': $scope.filetypes[0]
            }
        };
    }]);
