/****************************************************************************************
 * Copyright (c) 2014 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
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

describe('FindecoGraphDataService', function () {
    var graphDataService, httpBackend;

    //excuted before each "it" is run.
    beforeEach(function () {
        //load the module.
        angular.mock.module('Findeco');  // For Navigator
        angular.mock.module('FindecoGraphDataService');

        //inject your service for testing.
        angular.mock.inject(function ($httpBackend, GraphData) {
            graphDataService = GraphData;
            httpBackend = $httpBackend
        });
    });

/////////////////////////// loadGraphData /////////////////////////////
    describe('loadGraphData', function () {
        it('should have a loadGraphData function', function () {
            expect(angular.isFunction(graphDataService.loadGraphData)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadGraphData/withSpam/pa.1/th.2')
                .respond(200, {'loadGraphDataResponse': {'graphDataChildren': []}});
            graphDataService.loadGraphData('pa.1/th.2', 'withSpam');
            httpBackend.flush();
        });

        it('should work without supplying the type', function () {
            httpBackend.expectGET('/.loadGraphData/full/pa.1/th.2')
                .respond(200, {'loadGraphDataResponse': {'graphDataChildren': []}});

            graphDataService.loadGraphData('pa.1/th.2');
            httpBackend.flush();
        });
    });
});