/****************************************************************************************
 * Copyright (c) 2014 Klaus Greff, Johannes Merkert                                     *
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

function headerPosition() {
    var navigationBar = document.getElementById('navigationBar');
    if (navigationBar) {
        if (window.scrollY > document.getElementById('header').scrollHeight - 27) {
            navigationBar.style.position = 'fixed';
            navigationBar.style.top = '0';
            navigationBar.style.width = '100%';
        } else {
            navigationBar.style.position = 'relative';
            navigationBar.style.top = '-3px';
            navigationBar.style.width = 'auto';
        }
    }
}

function footerPosition() {
    var body = document.body;
    var html = document.documentElement;
    var documentHeight = Math.max(
            body.scrollHeight,
            body.offsetHeight,
            html.clientHeight,
            html.scrollHeight,
            html.offsetHeight);
    document.getElementById('footer').style.bottom = '-' + String(
            Math.floor(Math.max(0,(documentHeight - window.innerHeight - window.scrollY)) / 2)
    ) + 'px';
}

var didScroll = false;
setTimeout(footerPosition, 1);
setInterval(function () {didScroll = true;}, 500);

window.onscroll = function () {
    didScroll = true;
};

setInterval(function() {
    if(didScroll) {
        didScroll = false;
        footerPosition();
        headerPosition();
    }
}, 30);