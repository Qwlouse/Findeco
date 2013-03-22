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
/* Services */


angular.module('FindecoUserService', ['FindecoService'])
    .factory('FindecoUserService', function (FindecoService) {
        var localData = {};
        var localSetContent = function(data) {
            localData.content = data;
            if ( angular.equals(localData.content,{}) ) {
                localData.isLoggedIn = false;
            } else {
                localData.isLoggedIn = true;
            }
        };
        return {
            data: localData,
            setContent: localSetContent,
            initialize: function(){
                FindecoService.loadUserSettings().success( function (data) {
                    localSetContent(data.loadUserSettingsResponse);
                });
            }
        };
    });