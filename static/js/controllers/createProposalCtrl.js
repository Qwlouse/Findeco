/****************************************************************************************
 * Copyright (c) 2014  Klaus Greff, Maik Nauheim, Johannes Merkert                      *
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

findecoApp.controller(
    'FindecoCreateProposalCtrl',
    function ($scope, $routeParams, Backend, Message, Navigator, CVST, User) {
        $scope.getNodePath = function () {
            return Navigator.nodePath;
        };
        $scope.isRefinement = function () {
            return $scope.proposalType == 'refinement';
        };
        $scope.step = 1;
        $scope.heading = "";
        $scope.text = "";
        $scope.subsections = [];
        $scope.onlineState = {
            heading: "",
            text: "",
            subsections: []
        };
        $scope.dragPosition = 0;
        $scope.error = undefined;

        if (!User.isLoggedIn) {
            Navigator.changePath(Navigator.nodePath);
        }

        $scope.setProposalType = function (type) {
            $scope.proposalType = type;
            var paragraphs = [];
            if (type == 'refinement') {
                Backend.loadText(paragraphs, Navigator.nodePath).success(function () {
                    var headingRegex = /^.*=+\s*\[\[.+\|(.*)\]\]\s*=+((?:\n|\r|.)*)$/;
                    var matches = headingRegex.exec(paragraphs[0].wikiText);
                    $scope.heading = matches[1];
                    $scope.text = matches[2];
                    paragraphs.splice(0, 1);
                    $scope.subsections = [];
                    for (var i = 0; i < paragraphs.length; i++) {
                        if (RegExp("^" + Navigator.nodePath.replace(/\./g, "\\.") +
                            "/?[A-Za-z0-9-_]+\\.\\d+$").test(paragraphs[i].path)) {
                            matches = RegExp("^" + Navigator.nodePath.replace(/\./g, "\\.") +
                                "/?([A-Za-z0-9-_]+)\\.\\d+$").exec(paragraphs[i].path);
                            $scope.subsections.push({
                                heading: headingRegex.exec(paragraphs[i].wikiText)[1],
                                shorttitle: matches[1]
                            });
                        }
                    }
                    $scope.onlineState = {
                        heading: angular.copy($scope.heading),
                        text: angular.copy($scope.text),
                        subsections: angular.copy($scope.subsections)
                    };
                });
            }
            if (type == 'proposal') {
                $scope.heading = "";
                $scope.text = "";
                $scope.subsections = [];
                $scope.onlineState = {
                    heading: "",
                    text: "",
                    subsections: []
                };
            }
            $scope.step++;
        };

        $scope.nextStep = function () {
            if ((($scope.step == 2) && $scope.proposalIsChanged() &&
                $scope.proposalHasSufficientText() && $scope.checkAllShorttitles()) ||
                (($scope.step == 3) && $scope.argumentHasText())) {
                $scope.step++;
                if (($scope.step == 3) && ($scope.proposalType != 'refinement')) {
                    $scope.step++;
                }
            }
        };

        $scope.setStep = function (step) {
            if ((step < $scope.step) && (step > 0)) {
                $scope.step = step;
            }
        };

        $scope.previousStep = function () {
            $scope.step--;
            if (($scope.step == 3) && ($scope.proposalType != 'refinement')) {
                $scope.step--;
            }
        };

        $scope.proposalHasSufficientText = function () {
            if (!((angular.isString($scope.heading)) && (angular.isString($scope.text)) &&
                    ($scope.heading.length > 2) && ($scope.text.length > 2))) {
                return false;
            }
            if ($scope.text.match(/^\s*(={1,6}[^=]+=*)\s*$/m)) {
                return false;
            }
            for (var i = 0; i < $scope.subsections.length; i++) {
                var checkSubsectionForSufficientText = function (subsection) {
                    if (subsection.newSection) {
                        if (!(angular.isString(subsection.heading) &&
                             (subsection.heading.length > 2) &&
                             angular.isString(subsection.text) &&
                             (subsection.text.length > 2))) {
                            return false;
                        }
                        if (subsection.text.match(/^\s*(={1,6}[^=]+=*)\s*$/m)) {
                            return false;
                        }
                    }
                    if (subsection.newSection && subsection.subsections &&
                        angular.isArray(subsection.subsections)) {
                        for (var i = 0; i < subsection.subsections.length; i++) {
                            if (!checkSubsectionForSufficientText(subsection.subsections[i])) {
                                return false;
                            }
                        }
                    }
                    return true;
                };
                if (!checkSubsectionForSufficientText($scope.subsections[i])) {
                    return false;
                }
            }
            return true;
        };

        $scope.proposalIsChanged = function () {
            if (!angular.equals($scope.onlineState.heading, $scope.heading)) {
                return true;
            }
            if (!angular.equals($scope.onlineState.text, $scope.text)) {
                return true;
            }
            if ($scope.subsections.length != $scope.onlineState.subsections.length) {
                return true;
            }
            for (var i = 0; i < $scope.subsections.length; i++) {
                if (!angular.equals($scope.subsections[i], $scope.onlineState.subsections[i])) {
                    return true;
                }
            }
            return false;
        };

        $scope.argumentHasText = function () {
            return ((angular.isString($scope.argumentTitle)) && (angular.isString($scope.argumentText)) &&
                    ($scope.argumentTitle.length > 2) && ($scope.argumentText.length > 2));
        };

        $scope.startDrag = function ($event, subsection, subsections, index) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.dragInfo = {
                y: $event.clientY,
                grabOffset: $event.clientY - $event.target.getBoundingClientRect().top,
                subSection: subsection,
                subSections: subsections,
                index: index
            };
        };

        $scope.drag = function ($event) {
            $event.stopPropagation();
            if ($scope.dragInfo) {
                var subsections = $scope.dragInfo.subSections;
                $scope.dragPosition = $event.clientY - $scope.dragInfo.y;
                var prevTop = -1000;
                var prevHeight = 0;
                var nextTop = 10000;
                var nextHeight = 0;
                var myTop = 0;
                var myHeight = 0;
                var i = 0;
                var rect;
                var parentUl = $event.target.parentNode;
                while (parentUl.nodeName != 'UL') {
                    parentUl = parentUl.parentNode;
                }
                angular.forEach(parentUl.childNodes, function (node) {
                    if ((node.nodeType == 1) && (i < subsections.length)) {
                        rect = node.getBoundingClientRect();
                        if (i == $scope.dragInfo.index - 1) {
                            prevTop = rect.top;
                            prevHeight = rect.bottom - rect.top;
                        }
                        if (i == $scope.dragInfo.index) {
                            myTop = rect.top;
                            myHeight = rect.bottom - rect.top;
                        }
                        if (i == $scope.dragInfo.index + 1) {
                            nextTop = rect.top;
                            nextHeight = rect.bottom - rect.top;
                        }
                        i++;
                    }
                });
                if (myTop < prevTop + Math.min(myHeight, prevHeight) / 2) {
                    $scope.dragPosition = myTop - prevTop;
                    $scope.dragInfo.y = prevTop + $scope.dragInfo.grabOffset;
                    subsections.splice($scope.dragInfo.index, 1);
                    $scope.dragInfo.index--;
                    subsections.splice($scope.dragInfo.index, 0, $scope.dragInfo.subSection);
                } else if (myTop > nextTop - Math.min(myHeight, nextHeight) / 2) {
                    $scope.dragPosition = myTop - nextTop;
                    $scope.dragInfo.y = nextTop + $scope.dragInfo.grabOffset + nextHeight - myHeight;
                    subsections.splice($scope.dragInfo.index, 1);
                    $scope.dragInfo.index++;
                    subsections.splice($scope.dragInfo.index, 0, $scope.dragInfo.subSection);
                }
            }
        };

        $scope.stopDrag = function () {
            $scope.dragInfo = undefined;
            $scope.dragPosition = 0;
        };

        $scope.deleteSubSection = function (subsections, index) {
            subsections.splice(index, 1);
        };

        $scope.addSubSection = function (subsections) {
            subsections.push({
                newSection: true,
                shorttitle: "",
                heading: "",
                text: "",
                subsections: []
            });
        };

        $scope.checkShorttitle = function (shorttitle, subsections) {
            if (!shorttitle) {
                return true;
            }
            if (angular.equals($scope.subsections, subsections)) {
                if ($scope.onlineState) {
                    angular.forEach($scope.onlineState.subsections, function (subsection) {
                        if (subsection.shorttitle == shorttitle) {
                            return false;
                        }
                    });
                }
            }
            var count = 0;
            angular.forEach(subsections, function(subsection) {
                if (subsection.shorttitle == shorttitle) {
                    count++;
                }
            });
            return count <= 1;
        };

        $scope.checkAllShorttitles = function () {
            var checkSubsections = function (subsections) {
                for (var i = 0; i < subsections.length; i++) {
                    if (!$scope.checkShorttitle(subsections[i].shorttitle, subsections)) {
                        return false;
                    }
                    if (subsections[i].subsections &&
                        angular.isArray(subsections[i].subsections) &&
                        (subsections[i].subsections.length > 0)) {
                        if (!checkSubsections(subsections[i].subsections)) {
                            return false;
                        }
                    }
                }
                return true;
            };
            return checkSubsections($scope.subsections);
        };

        $scope.createShortTitle = function (longTitle) {
            return CVST.createValidShortTitle(longTitle);
        };

        $scope.createWikiText = function () {
            var createWikiTextSubsections = function(headingLevel, subsections) {
                var i, j;
                var wikiText = "";
                for (i = 0; i < subsections.length; i++) {
                    for (j = 0; j < headingLevel; j++) {
                        wikiText = wikiText + "=";
                    }
                    wikiText = wikiText + " " + subsections[i].heading + " ";
                    for (j = 0; j < headingLevel; j++) {
                        wikiText = wikiText + "=";
                    }
                    wikiText = wikiText + "\n";
                    if (subsections[i].newSection) {
                        wikiText = wikiText + subsections[i].text + "\n";
                        if (subsections[i].subsections.length > 0) {
                            wikiText = wikiText +
                                createWikiTextSubsections(headingLevel + 1, subsections[i].subsections) + "\n\n";
                        }
                    } else {
                        wikiText = wikiText + "...\n\n";
                    }
                }
                return wikiText;
            };
            var wikiText = "";
            wikiText = wikiText + "= " + $scope.heading + " =\n";
            wikiText = wikiText + $scope.text + "\n";
            wikiText = wikiText + createWikiTextSubsections(2, $scope.subsections) + "\n\n";
            return wikiText;
        };

        $scope.submit = function () {
            var createSubsectionStructure = function (subsections) {
                var subsectionList = [];
                for (var i = 0; i < subsections.length; i++) {
                    var structure = {};
                    if (subsections[i].newSection) {
                        structure.heading = subsections[i].heading;
                        structure.text = subsections[i].text;
                    }
                    if (subsections[i].shorttitle) {
                        structure.shorttitle = subsections[i].shorttitle;
                    } else {
                        structure.shorttitle = CVST.createValidShortTitle(subsections[i].heading);
                    }
                    if (subsections[i].subsections && angular.isArray(subsections[i].subsections)) {
                        structure.subsections = createSubsectionStructure(subsections[i].subsections);
                    }
                    subsectionList.push(structure);
                }
                return subsectionList;
            };
            var submitData = {
                proposal: {
                    heading: $scope.heading,
                    text: $scope.text,
                    subsections: createSubsectionStructure($scope.subsections)
                }
            };
            if ($scope.proposalType == 'refinement') {
                submitData.argument = {
                    heading: $scope.argumentTitle,
                    text: $scope.argumentText
                };
            }
            $scope.submitting = true;
            var promise;
            $scope.error = undefined;
            if ($scope.proposalType == 'refinement') {
                promise = Backend.storeRefinement(Navigator.nodePath, submitData);
                promise.success(function (data) {
                    $scope.submitting = undefined;
                    Navigator.changePath(data.storeRefinementResponse.path);
                });
            } else {
                promise = Backend.storeProposal(Navigator.nodePath, submitData);
                promise.success(function (data) {
                    $scope.submitting = undefined;
                    Navigator.changePath(data.storeProposalResponse.path);
                });
            }
            promise.error(function (response) {
                $scope.submitting = undefined;
                $scope.error = response['errorResponse'];
            });
        };

        $scope.cancelProposal = function () {
            Navigator.changePath(Navigator.nodePath);
        }
    });

