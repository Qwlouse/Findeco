/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert, Klaus Greff, Maik Nauheim                         *
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
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/

/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

'use strict';
/* App Module */

var findecoApp = angular.module('Findeco', ['FindecoServices', 'localization', 'ui.bootstrap'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.
            when('/argument*param', {templateUrl: 'static/partials/default.html', controller: FindecoArgumentCtrl}).
            when('/createArgument*param', {templateUrl: 'static/partials/createArgument.html', controller: FindecoCreateCtrl}).
            when('/createAlternativeText*param', {templateUrl: 'static/partials/createAlternativeText.html', controller: FindecoCreateCtrl}).
            when('/createNewText*param', {templateUrl: 'static/partials/createNewText.html', controller: FindecoCreateCtrl}).
            when('/credits', {templateUrl: 'static/partials/credits.html', controller: FindecoDefaultCtrl}).
            when('/datenschutz', {templateUrl: 'static/partials/datenschutz.html', controller: FindecoDefaultCtrl}).
            when('/home', {templateUrl: 'static/partials/home.html', controller: FindecoDefaultCtrl}).
            when('/impressum', {templateUrl: 'static/partials/impressum.html', controller: FindecoDefaultCtrl}).
            when('/info*name', {templateUrl: 'static/partials/info.html', controller: FindecoUserInfoCtrl}).
            when('/kontakt', {templateUrl: 'static/partials/kontakt.html', controller: FindecoDefaultCtrl}).
            when('/login', {templateUrl: 'static/partials/userLogin.html', controller: FindecoUserCtrl}).
            when('/register', {templateUrl: 'static/partials/userRegistration.html', controller: FindecoUserCtrl}).
            when('/activate/*param', {templateUrl: 'static/partials/userActivate.html', controller: FindecoUserCtrl}).
            when('/nutzungsbedingungen', {templateUrl: 'static/partials/nutzungsbedingungen.html', controller: FindecoDefaultCtrl}).
            when('/profile', {templateUrl: 'static/partials/profile.html', controller: FindecoUserCtrl}).
            when('/start', {templateUrl: 'static/partials/start.html', controller: FindecoStartCtrl}).
            otherwise({templateUrl: 'static/partials/default.html', controller: FindecoDefaultCtrl});
    }]);