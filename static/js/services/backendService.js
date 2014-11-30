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

'use strict';
/**
 *  Backend wraps the the JSON API to the backend.
 *  It provides easy to use functions like logout() or
 *  loadText(paragraphList, path).
 *
 *  Those functions return a $http promise object, on which you can add
 *  callbacks for success and failure like this:
 *
 *  Backend.logout().success( function (data, status, headers, config) {
 *      alert("goodbye");
 *  }).error( function (data, status, headers, config) {
 *      alert("logout failed");
 *  });
 *
 *  Those get called once the request finished.
 *
 *  When there is data to be returned, the first parameter to the function
 *  (typically suffixed with _out) is the object/array the function writes its
 *  results to.
 *
 *  This service is stateless.
 *
 **/
angular.module('FindecoBackendService', [])
    .factory('Backend', function ($http) {
        function fillArray(array, attributes) {
            return function (data) {
                for (var i = 0; i < attributes.length; ++i) {
                    data = data[attributes[i]];
                }
                array.length = 0;
                angular.forEach(data, function (item) {
                    array.push(item);
                });
            }
        }

        function filterMicroblogging(data, microblogList_out) {
            angular.forEach(data['loadMicrobloggingResponse'], function (item) {
                var flag = false;
                angular.forEach(microblogList_out, function (oldItem) {
                    if (oldItem.microblogID == item.microblogID) {
                        flag = true;
                    }
                });
                if (!flag) {
                    var authors = [];
                    angular.forEach(item.authorGroup, function (authorName) {
                        var author = {};
                        author.displayName = authorName;
                        authors.push(author);
                    });
                    item.authorGroup = authors;
                    microblogList_out.push(item);
                }
            });
            microblogList_out = microblogList_out.sort(function (a, b) {
                return b.microblogID - a.microblogID;
            });
        }

        function addIdTypeAndGetPromise(microblogList_out, url, id, type) {
            var idParam = 'id=-1&';
            if (id != undefined && id != 0) {
                idParam = 'id=' + id + '&';
            }
            if (type == undefined) {
                type = "newer";
            }
            var promise = $http.get(url + '?' + idParam + 'type=' + type);
            promise.success(function (data) {
                filterMicroblogging(data, microblogList_out);
            });
            return promise;
        }

        return {
            loadAnnounce: function () {
                return $http.get('/static/externaljson/info.json');
            },

            loadMicrobloggingForFollowedNodes: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingForFollowedNodes/' + name + '/';
                return addIdTypeAndGetPromise(microblogList_out, path, id, type);
            },

            loadMicrobloggingForAllNodes: function (microblogList_out, id, type) {
                var path = '/.loadMicrobloggingAll/';
                return addIdTypeAndGetPromise(microblogList_out, path, id, type);
            },

            loadMicrobloggingForAuthoredNodes: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingForAuthoredNodes/' + name + '/';
                return addIdTypeAndGetPromise(microblogList_out, path, id, type);
            },

            loadMicrobloggingMentions: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingMentions/' + name + '/';
                return addIdTypeAndGetPromise(microblogList_out, path, id, type);
            },

            loadMicrobloggingTimeline: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingTimeline/' + name + '/';
                return addIdTypeAndGetPromise(microblogList_out, path, id, type);
            },

            loadMicrobloggingFromUser: function (microblogList_out, name, id, type) {
                var path = '/.loadMicrobloggingFromUser/' + name + '/';
                return addIdTypeAndGetPromise(microblogList_out, path, id, type);
            },

            loadMicrobloggingForNode: function (microblogList_out, path, id, type) {
                var url_part = '/.loadMicrobloggingForNode/' + path;
                return addIdTypeAndGetPromise(microblogList_out, url_part, id, type);
            },

            markNode: function (markType, nodePath) {
                var pathComponents = ['/.markNode', markType, nodePath];
                var url = pathComponents.join('/');
                url = url.replace("//", "/");
                return $http.get(url);
            },

            storeMicroblogging: function (path, microblogText) {
                var pathComponents = ['/.storeMicroblogging', path];
                var url = pathComponents.join('/');
                //url = url.replace("//","/");
                return $http.post(url, {microblogText: microblogText});
            },

            storeRefinement: function (path, data) {
                var pathComponents = ['/.storeRefinement', path];
                var url = pathComponents.join('/');
                url = url.replace("//", "/");
                return $http.post(url, data);
            },

            storeText: function (path, params) {
                var pathComponents = ['/.storeText', path];
                var url = pathComponents.join('/');
                url = url.replace("//", "/");
                return $http.post(url, params);
            },

            loadArgument: function (indexNodes_out, path) {
                var url = ['/.loadArgumentIndex', path].join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);
                promise.success(fillArray(indexNodes_out,
                    ['loadArgumentIndexResponse']));
                return promise;
            },

            loadText: function (paragraphList_out, path) {
                var url = ['/.loadText', path].join('/');
                url = url.replace("//", "/");
                var promise = $http.get(url);
                promise.success(fillArray(paragraphList_out,
                    ['loadTextResponse', 'paragraphs']));
                return promise;
            },

            loadUserInfo: function (user) {
                var url = ['/.loadUserInfo', user].join('/');
                url = url.replace("//", "/");
                return $http.get(url);
            },

            loadNode: function (nodeInfo, path) {
                var url = ['/.loadNode', path].join('/');
                var promise = $http.get(url);
                promise.success(function (d) {
                    angular.copy(d.loadNodeResponse, nodeInfo);
                    nodeInfo.path = path
                });
                return promise;
            },
            loadArgumentNews: function (cards) {
                var promise = $http.get('/.loadArgumentNews');
                promise.success(function (d) {
                    angular.copy(d.loadArgumentNewsResponse, cards);
                });
                return promise;
            },
            search: function (searchResults, search_string) {
                var searchFields = "user_content_microblogging";
                var promise = $http.get('/.search/' + searchFields + '/' + search_string);

                promise.success(function (d) {
                    angular.copy(d.searchResponse, searchResults);
                });
                return promise;
            }
        };
    })
;