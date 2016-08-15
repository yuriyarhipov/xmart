  /* ============================================================
 * File: app.js
 * Configure global module dependencies. Page specific modules
 * will be loaded on demand using ocLazyLoad
 * ============================================================ */

'use strict';

angular.module('app', [
    'ui.router',
    'ui.utils',
    'oc.lazyLoad',
    'angular-jwt',
    'angularFileUpload',
    'ui.grid',
    'ui.grid.resizeColumns',
    'ngCookies',
]);
