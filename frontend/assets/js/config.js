/* ============================================================
 * File: config.js
 * Configure routing
 * ============================================================ */

angular.module('app')
    .config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$httpProvider',

        function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

            $urlRouterProvider
                .otherwise('/login');

            $stateProvider
                .state('app', {
                    abstract: true,
                    url: "/app",
                    templateUrl: "tpl/app.html"
                })
                .state('app.projects', {
                    url: "/projects",
                    templateUrl: "tpl/projects.html",
                    controller: 'ProjectsCtrl',
                    resolve: {
                        deps: ['$ocLazyLoad', function($ocLazyLoad) {
                            return $ocLazyLoad.load([
                                    'nestable'
                                ], {
                                    insertBefore: '#lazyload_placeholder'
                                })
                                .then(function() {
                                    return $ocLazyLoad.load('assets/js/controllers/projects.js');
                                });
                        }]
                    }
                })
                .state('app.create_project', {
                    url: "/create_project",
                    templateUrl: "tpl/create_project.html",
                    controller: 'CreateProjectCtrl',
                    resolve: {
                        deps: ['$ocLazyLoad', function($ocLazyLoad) {
                            return $ocLazyLoad.load([
                                    'nestable'
                                ], {
                                    insertBefore: '#lazyload_placeholder'
                                })
                                .then(function() {
                                    return $ocLazyLoad.load('assets/js/controllers/projects.js');
                                });
                        }]
                    }
                })
                .state('app.fileshub', {
                    url: "/fileshub",
                    templateUrl: "tpl/files_hub.html",
                    controller: 'FilesHubCtrl',
                    resolve: {
                        deps: ['$ocLazyLoad', function($ocLazyLoad) {
                            return $ocLazyLoad.load([
                                    'nestable',
                                    'select'
                                ], {
                                    insertBefore: '#lazyload_placeholder'
                                })
                                .then(function() {
                                    return $ocLazyLoad.load('assets/js/controllers/fileshub.js');
                                });
                        }]
                    }
                })
                .state('login', {
                    url: "/login",
                    templateUrl: "tpl/login.html",
                    controller: 'LoginCtrl',
                })
                .state('app.changePass', {
                    url: "/change_pass",
                    templateUrl: "tpl/change_pass.html",
                    controller: 'ChangePassCtrl',
                });

        }
    ]);
