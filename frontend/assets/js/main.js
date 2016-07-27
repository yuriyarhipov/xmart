/* ============================================================
 * File: main.js
 * Main Controller to set global scope variables.
 * ============================================================ */

angular.module('app')
    .config(function Config($httpProvider, jwtInterceptorProvider) {
        jwtInterceptorProvider.tokenGetter = ['config', function (config) {
            if (config.url.substr(config.url.length - 5) == '.html') {
                return null;
            }
            return localStorage.getItem('id_token');
        }];

        $httpProvider.interceptors.push('jwtInterceptor');
    })    
    .controller('AppCtrl', ['$scope', '$rootScope', '$state', 'jwtHelper', '$window', function ($scope, $rootScope, $state, jwtHelper, $window) {
        // App globals
        var username;
        var token = localStorage.getItem('id_token');        
        if (token){
            username = jwtHelper.decodeToken(token).username;
        } else {
            $window.location.href ='#/login';
        }        
        $scope.app = {
            name: 'Xmart Parser',
            user: username,
            description: 'Xmart Dashboard',
            layout: {
                menuPin: false,
                menuBehind: false,
                theme: 'pages/css/pages.css'
            },
            author: 'Brightcomms'
        }

        // Checks if the given state is the current state
        $scope.is = function (name) {
            return $state.is(name);
        }

        // Checks if the given state/child states are present
        $scope.includes = function (name) {
            return $state.includes(name);
        }

        // Broadcasts a message to pgSearch directive to toggle search overlay
        $scope.showSearchOverlay = function () {
            $scope.$broadcast('toggleSearchOverlay', {
                show: false
            })
        }

        $scope.logout = function(){
            localStorage.removeItem("id_token");
            $window.location.href ='#/login';
        };

    }]);


angular.module('app')
    /*
        Use this directive together with ng-include to include a
        template file by replacing the placeholder element
    */

    .directive('includeReplace', function () {
        return {
            require: 'ngInclude',
            restrict: 'A',
            link: function (scope, el, attrs) {
                el.replaceWith(el.children());
            }
        };
    })
