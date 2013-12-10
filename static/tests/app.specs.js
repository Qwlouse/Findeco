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

describe("Findeco Module", function() {
    var m;
    beforeEach(function() {
      m = angular.module("Findeco");
    });

    it("should be registered", function() {
      expect(m).not.toBe(null);
        alert(m);
    });

//    describe("Dependencies:", function() {
//
//      var deps;
//      var hasModule = function(m) {
//        return deps.indexOf(m) >= 0;
//      };
//      before(function() {
//        deps = module.value('appName').requires;
//      });
//
//      //you can also test the module's dependencies
//      it("should have App.Controllers as a dependency", function() {
//        expect(hasModule('App.Controllers')).to.equal(true);
//      });
//
//      it("should have App.Directives as a dependency", function() {
//        expect(hasModule('App.Directives')).to.equal(true);
//      });
//
//      it("should have App.Filters as a dependency", function() {
//        expect(hasModule('App.Filters')).to.equal(true);
//      });
//
//      it("should have App.Routes as a dependency", function() {
//        expect(hasModule('App.Routes')).to.equal(true);
//      });
//
//      it("should have App.Services as a dependency", function() {
//        expect(hasModule('App.Services')).to.equal(true);
//      });
//    });
});
