#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2013 Michael Zaspel <michaelzaspel@web.de.de>
# This file is part of Findeco.
#
# Findeco is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# Findeco is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Findeco. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#endregion #####################################################################
from django.test import LiveServerTestCase
from nose.plugins.attrib import attr
from test_helper import helper_login_admin
from selenium import webdriver
from BeautifulSoup import BeautifulSoup, SoupStrainer
import lxml.html
import time


@attr('selenium')
class TestFeLocalization(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()

    def test_profile_localizations(self):
        """
        Checks all listed Pages for missing localization strings.
        @param self:
        """
        helper_login_admin(self)
        time.sleep(1)
        pages=["/microblogging","/Spielwiese.1"
            ]


        pages_exclude = ["/terms_of_use", "/data_privacy"]

        done=[""]
        while pages:
            for page in pages:

                self.driver.get(self.live_server_url + page)
                time.sleep(2)
                self.assertNotIn('_', self.driver.find_element_by_tag_name('body').text, "Localization missing in " + page)
                pages.remove(page)
                done.append(page)
                elem = self.driver.find_element_by_xpath("//*")
                contents = elem.get_attribute("innerHTML")
                dom = lxml.html.fromstring(contents)
                for link in dom.xpath('//a/@href'):

                    if (link <> "#")and(link<>" ") and not ( "http:" in link) and not ( "https:" in link) and not (link in pages) and not (link in done) and not (
                            link in pages_exclude) and not ("static" in link) and not ("{{"in link):
                        if (link=="/static/customContent/imprint.html"):
                            print "foolpage"+page
                        print link

                        pages.append(link)
