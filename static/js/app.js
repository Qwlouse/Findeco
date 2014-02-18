/****************************************************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim, Johannes Merkert       *
 *                                                                                      *
 * This file is part of Findeco.                                                        *
 *                                                                                      *
 * Findeco is free software; you can redistribute it and/or modify it under             *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * Findeco is distributed in the hope that it will be useful, but WITHOUT ANY           *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * Findeco. If not, see <http://www.gnu.org/licenses/>.                                 *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

'use strict';

var findecoApp = angular.module(
        'Findeco',
        ['ngAnimate',
         'ngRoute',
         'FindecoServices',
         'FindecoBackendService',
         'FindecoUserService',
         'FindecoNavigatorService',
         'localization',
         'ui.bootstrap']
    )
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/create/:type/:param*', {templateUrl: '/static/partials/create.html', controller: 'FindecoCreateCtrl'}).
            when('/about', {templateUrl: '/static/partials/about.html', controller: 'FindecoCustomContentCtrl'}).
            when('/diff/:param*', {templateUrl: '/static/partials/diff.html', controller: 'FindecoDiffCtrl'}).
            when('/data_privacy', {templateUrl: '/static/partials/dataPrivacy.html', controller: 'FindecoCustomContentCtrl'}).
            when('/imprint', {templateUrl: '/static/partials/imprint.html', controller: 'FindecoCustomContentCtrl'}).
            when('/user/:name*', {templateUrl: '/static/partials/user.html', controller: 'FindecoUserInfoCtrl'}).
            when('/login', {templateUrl: '/static/partials/userLogin.html', controller: 'FindecoUserCtrl'}).
            when('/register', {templateUrl: '/static/partials/userRegistration.html', controller: 'FindecoUserCtrl'}).
            when('/activate/:param*', {templateUrl: '/static/partials/activate.html', controller: 'FindecoConfirmationCtrl'}).
            when('/confirm_email/:param*', {templateUrl: '/static/partials/activate.html', controller: 'FindecoConfirmationCtrl'}).
            when('/confirm/:param*', {templateUrl: '/static/partials/activate.html', controller: 'FindecoConfirmationCtrl'}).
            when('/recoverByMail', {templateUrl: '/static/partials/userRecoverByMail.html', controller: 'FindecoUserCtrl'}).
            when('/recoverByUsername', {templateUrl: '/static/partials/userRecoverByUsername.html', controller: 'FindecoUserCtrl'}).
            when('/terms_of_use', {templateUrl: '/static/partials/termsOfUse.html', controller: 'FindecoCustomContentCtrl'}).
            when('/profile', {templateUrl: '/static/partials/profile/profile.html', controller: 'FindecoUserCtrl'}).
            when('/profile/account', {templateUrl: '/static/partials/profile/profile.html', controller: 'FindecoUserCtrl'}).
            when('/profile/password', {templateUrl: '/static/partials/profile/profilePassword.html', controller: 'FindecoUserCtrl'}).
            when('/profile/mail', {templateUrl: '/static/partials/profile/profileMailSettings.html', controller: 'FindecoUserCtrl'}).
            when('/profile/delete', {templateUrl: '/static/partials/profile/profileDelete.html', controller: 'FindecoUserCtrl'}).
            when('/news', {templateUrl: '/static/partials/news.html', controller: FindecoNewsCtrl}).
            when('/microblogging', {templateUrl: '/static/partials/microbloggingNews.html', controller: 'FindecoMicrobloggingNewsCtrl'}).
            when('/search/:searchString*', {templateUrl: '/static/partials/searchResults.html', controller: FindecoSearchCtrl}).
            when('/', {templateUrl: '/static/partials/start.html', controller: 'FindecoDefaultCtrl'}).
            when('/start', {templateUrl: '/static/partials/start.html', controller: 'FindecoDefaultCtrl'}).
            when('/index', {templateUrl: '/static/partials/startDefault.html', controller: 'FindecoDefaultCtrl'}).
            when('/index.htm', {templateUrl: '/static/partials/startDefault.html', controller: 'FindecoDefaultCtrl'}).
            when('/index.html', {templateUrl: '/static/partials/startDefault.html', controller: 'FindecoDefaultCtrl'}).
            otherwise({templateUrl: '/static/partials/default.html', controller: 'FindecoDefaultCtrl'});
    }]);

findecoApp.constant('Version','0.4.0-alpha');
