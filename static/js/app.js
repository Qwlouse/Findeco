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
         'FindecoSettings',
         'FindecoBackendService',
         'FindecoUserService',
         'FindecoNavigatorService',
         'FindecoGraphDataService',
         'FindecoCreateValidShortTitle',
         'localization',
         'ui.bootstrap']
    )
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/old/create/:type/:param*', {templateUrl: '/static/partials/create.html', controller: 'FindecoCreateCtrl'}).
            when('/about', {templateUrl: '/static/partials/about.html', controller: 'FindecoCustomContentCtrl'}).
            when('/diff/:param*', {templateUrl: '/static/partials/diff.html', controller: 'FindecoDiffCtrl'}).
            when('/data_privacy', {templateUrl: '/static/partials/dataPrivacy.html', controller: 'FindecoCustomContentCtrl'}).
            when('/imprint', {templateUrl: '/static/partials/imprint.html', controller: 'FindecoCustomContentCtrl'}).
            when('/user/:name*', {templateUrl: '/static/partials/user.html', controller: 'FindecoUserInfoCtrl'}).
            when('/login', {templateUrl: '/static/partials/userLogin.html', controller: 'FindecoUserCtrl'}).
            when('/register', {templateUrl: '/static/partials/userRegistration.html', controller: 'FindecoUserCtrl'}).
            when('/registerSuccess', {templateUrl: '/static/partials/registerSuccess.html'}).
            when('/activate/:param?', {templateUrl: '/static/partials/activate.html', controller: 'FindecoConfirmationCtrl'}).
            when('/confirm_email/:param?', {templateUrl: '/static/partials/activate.html', controller: 'FindecoConfirmationCtrl'}).
            when('/confirm/:param?', {templateUrl: '/static/partials/activate.html', controller: 'FindecoConfirmationCtrl'}).
            when('/recoverByMail', {templateUrl: '/static/partials/userRecoverByMail.html', controller: 'FindecoUserCtrl'}).
            when('/recoverByUsername', {templateUrl: '/static/partials/userRecoverByUsername.html', controller: 'FindecoUserCtrl'}).
            when('/terms_of_use', {templateUrl: '/static/partials/termsOfUse.html', controller: 'FindecoCustomContentCtrl'}).
            when('/profile', {templateUrl: '/static/partials/profile.html', controller: 'FindecoUserCtrl'}).
            when('/news', {templateUrl: '/static/partials/news.html', controller: 'FindecoNewsCtrl'}).
            when('/microblogging', {templateUrl: '/static/partials/microbloggingNews.html', controller: 'FindecoMicrobloggingNewsCtrl'}).
            when('/arguments', {templateUrl: '/static/partials/argumentNews.html', controller: 'FindecoArgumentNewsCtrl'}).
            when('/', {templateUrl: '/static/partials/indexPage.html', controller: 'FindecoArgumentNewsCtrl'}).
            when('/search/:searchString*', {templateUrl: '/static/partials/searchResults.html', controller: 'FindecoSearchCtrl'}).
            when('/start', {templateUrl: '/static/partials/start.html', controller: 'FindecoDefaultCtrl'}).
            when('/index', {templateUrl: '/static/partials/startDefault.html', controller: 'FindecoDefaultCtrl'}).
            when('/index.htm', {templateUrl: '/static/partials/startDefault.html', controller: 'FindecoDefaultCtrl'}).
            when('/index.html', {templateUrl: '/static/partials/startDefault.html', controller: 'FindecoDefaultCtrl'}).
            when('/create/proposal/:param*', {templateUrl: '/static/partials/create/proposalWizzard.html', controller: 'FindecoCreateProposalCtrl'}).
            when('/create/argument/:param*', {templateUrl: '/static/partials/create/argumentWizzard.html', controller: 'FindecoCreateArgumentCtrl'}).
            otherwise({templateUrl: '/static/partials/default.html', controller: 'FindecoDefaultCtrl'});
    }]);

findecoApp.run(function ($rootScope, localize, Fesettings) {
    $rootScope.$watch('language', function (newLang) {
        localize.setLanguage(newLang);
        $rootScope.$broadcast('langChange', newLang);
    });
    // initialization
    if (!$rootScope.language &&
        angular.isArray(Fesettings.activatedLanguages) &&
        (Fesettings.activatedLanguages.length > 0)) {
        $rootScope.language = Fesettings.activatedLanguages[0];
    }
});
