'use strict';

/* Controllers */

angular.module('app')
    .controller('FilesHubCtrl', ['$scope', '$http', 'FileUploader', '$interval', function($scope, $http, FileUploader, $interval) {
        $scope.vendors = ['Ericsson', 'Nokia', 'Huawei', 'Universal', ];
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
                    'Gpeh',
                ];
            }
            if  ($scope.vendor.selected == 'Nokia') {
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
        var token = localStorage.getItem('id_token');
        var uploader = $scope.uploader = new FileUploader({
            url: '/api/upload_file/',
            removeAfterUpload: true,
            withCredentials: true,
            headers: {
                'Authorization': 'Bearer ' + token,
            },
        });

        uploader.onAfterAddingFile = function(fileItem) {
            fileItem.formData.push({
                'description': $scope.description,
                'vendor': $scope.vendor.selected,
                'network': $scope.network.selected,
                'file_type': $scope.filetype.selected,
            });
        };

        $scope.uploadFile = function(){
            while (uploader.queue.length > 1){
                uploader.removeFromQueue(uploader.queue[0])
            }
            uploader.uploadAll()
            $http.get('/api/uploaded_files/').success(function(data){
                $scope.uploaded_files = data;
            });
        };
        var get_work_files = function(){
            $http.get('/api/work_files/').success(function(data){
                $scope.work_files = data;
            });
        };
        var get_uploaded_files = function(){
            $http.get('/api/uploaded_files/').success(function(data){
                $scope.uploaded_files = data;
            });
        };

        $interval(get_uploaded_files, 1000);
        $interval(get_work_files, 1000);

        $scope.onProcessAll = function(){
            $http.post('/api/process_all/').success(function(){
                get_uploaded_files();
            });
        };

        $scope.onDeleteAll = function(){
            for (var i in $scope.uploaded_files){
                $http.delete('/api/uploaded_files/' + $scope.uploaded_files[i].id + '/').success(function(){
                    get_uploaded_files();
                });
            }
        }


    }]);
