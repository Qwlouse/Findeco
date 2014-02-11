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

    ////////////////////////////// markNode ///////////////////////////////
    describe('markNode', function () {
        it('should have a markNode function', function () {
            expect(angular.isFunction(backendService.markNode)).toBe(true);
        });

        it('should call the right path', function () {
            var markTypes = ['follow', 'unfollow', 'spam', 'notspam'];
            for (var n = 0; n < markTypes.length; n++) {
                httpBackend.expectGET('/.json_markNode/' + markTypes[n] + '/pa.1/th.2').respond(200, {'call': 1});
                backendService.markNode(markTypes[n], 'pa.1/th.2').success(function (data) {
                    expect(data['call']).toBe(1);
                });
            }
            httpBackend.flush();
        });
    });

    //////////////////////// storeMicroblogging ///////////////////////////
    describe('storeMicroblogging', function () {
        it('should have a storeMicroblogging function', function () {
            expect(angular.isFunction(backendService.storeMicroblogging)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectPOST('/.storeMicroblogging/pa.1/th.2', {'microblogText': "Blubb"})
                .respond(200, {'call': 1});
            backendService.storeMicroblogging('pa.1/th.2', "Blubb").success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ///////////////////////////// storeText /////////////////////////////
    describe('storeText', function () {
        it('should have a storeText function', function () {
            expect(angular.isFunction(backendService.storeText)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectPOST('/.json_storeText/pa.1/th.2', {'param1': "Blupp", 'param2': 14})
                .respond(200, {'call': 1});
            backendService.storeText('pa.1/th.2', {'param1': "Blupp", 'param2': 14}).success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ////////////////////////// loadArgument /////////////////////////////
    describe('loadArgument', function () {
        it('should have a loadArgument function', function () {
            expect(angular.isFunction(backendService.loadArgument)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.json_loadArgumentIndex/pa.1/th.2').respond(200, {'call': 1});
            backendService.loadArgument([], 'pa.1/th.2').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });

    ////////////////////////// loadText /////////////////////////////
    describe('loadText', function () {
        it('should have a loadText function', function () {
            expect(angular.isFunction(backendService.loadText)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.json_loadText/pa.1/th.2')
                .respond(200, {'loadTextResponse': 1, 'paragraphs': ['1','3','4']});
            backendService.loadText([], 'pa.1/th.2').success(function (data) {
                expect(data['loadTextResponse']).toBe(1);
                var paragraphTexts = ['1','3','4'];
                for (var k = 0; k < data['paragraphs'].length; k++) {
                    expect(data['paragraphs'][k]).toBe(paragraphTexts[k]);
                }
            });
            httpBackend.flush();
        });
    });

    ////////////////////////// loadUserInfo /////////////////////////////
    describe('loadUserInfo', function () {
        it('should have a loadUserInfo function', function () {
            expect(angular.isFunction(backendService.loadUserInfo)).toBe(true);
        });

        it('should call the right path', function () {
            httpBackend.expectGET('/.json_loadUserInfo/max_mustermann').respond(200, {'call': 1});
            backendService.loadUserInfo('max_mustermann').success(function (data) {
                expect(data['call']).toBe(1);
            });
            httpBackend.flush();
        });
    });
});