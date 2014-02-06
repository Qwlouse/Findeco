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

describe('FindecoBackendService', function () {
    var backendService, httpBackend;

    //excuted before each "it" is run.
    beforeEach(function () {

        //load the module.
        angular.mock.module('FindecoBackendService');

        //inject your service for testing.
        angular.mock.inject(function ($httpBackend, Backend) {
            backendService = Backend;
            httpBackend = $httpBackend
        });
    });

    //////////////////////////////// loadAnnounce ///////////////////////////////////
    describe('loadAnnounce', function () {
        it('should have a loadAnnounce function', function () {
            expect(angular.isFunction(backendService.loadAnnounce)).toBe(true);
        });

        it('should return a promise with content', function () {
            httpBackend.expectGET('/static/externaljson/info.json').respond(200, {'b': 1});
            backendService.loadAnnounce().success(function (data) {
                expect(data['b']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingForFollowedNodes /////////////////////////
    describe('loadMicrobloggingForFollowedNodes', function () {
        it('should have a loadMicrobloggingForFollowedNodes function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingForFollowedNodes)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingForFollowedNodes/hugo/?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingForFollowedNodes([], 'hugo').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingForAllNodes /////////////////////////
    describe('loadMicrobloggingForAllNodes', function () {
        it('should have a loadMicrobloggingForAllNodes function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingForAllNodes)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingAll/?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingForAllNodes([]).success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingForAuthoredNodes /////////////////////////
    describe('loadMicrobloggingForAuthoredNodes', function () {
        it('should have a loadMicrobloggingForAuthoredNodes function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingForAuthoredNodes)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingForAuthoredNodes/hugo/?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingForAuthoredNodes([], 'hugo').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingMentions /////////////////////////
    describe('loadMicrobloggingMentions', function () {
        it('should have a loadMicrobloggingMentions function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingMentions)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingMentions/hugo/?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingMentions([], 'hugo').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingTimeline /////////////////////////
    describe('loadMicrobloggingTimeline', function () {
        it('should have a loadMicrobloggingTimeline function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingTimeline)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingTimeline/hugo/?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingTimeline([], 'hugo').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingFromUser /////////////////////////
    describe('loadMicrobloggingFromUser', function () {
        it('should have a loadMicrobloggingFromUser function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingFromUser)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingFromUser/hugo/?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingFromUser([], 'hugo').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////// loadMicrobloggingForNode /////////////////////////
    describe('loadMicrobloggingForNode', function () {
        it('should have a loadMicrobloggingForNode function', function () {
            expect(angular.isFunction(backendService.loadMicrobloggingForNode)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.loadMicrobloggingForNode/pa.1/th.2?id=-1&type=newer').respond(200, {'call': 1});
            backendService.loadMicrobloggingForNode([], 'pa.1/th.2').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });
});