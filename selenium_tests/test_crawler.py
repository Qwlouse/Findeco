#!/usr/bin/env python3
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
import lxml.html
import time
from node_storage import get_root_node
from node_storage.factory import create_textNode, create_slot, create_user
from node_storage.factory import create_vote


@attr('selenium')
class TestCrawler(LiveServerTestCase):
    #fixtures = ['test.json']
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234", groups=['voters'])
        self.permela = create_user("Permela", password="xxx")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla", "Blubb", [self.hugo])
        self.slot.append_child(self.text)
        self.mid = create_textNode("Bla derivate", "Blubb2", [self.hugo])
        self.slot.append_child(self.mid)
        self.text.add_derivate(self.mid, arg_type='n')
        self.leaf1 = create_textNode("Bla leaf 1", "Blubb3", [self.hugo])
        self.slot.append_child(self.leaf1)
        self.mid.add_derivate(self.leaf1, arg_type='n')
        self.mid2 = create_textNode("Bla derivate 2", "Blubb4", [self.hugo])
        self.slot.append_child(self.mid2)
        self.mid.add_derivate(self.mid2, arg_type='n')
        self.leaf2 = create_textNode("Bla leaf 2", "Blubb5", [self.hugo])
        self.slot.append_child(self.leaf2)
        self.mid2.add_derivate(self.leaf2, arg_type='n')
        self.follow = create_vote(self.hugo, [self.text, self.mid, self.leaf1, self.mid2, self.leaf2])

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()

    def test_crawl_test(self):
        """
        Checks all listed Pages for missing localization strings.
        @param self:
        """

        helper_login_admin(self)
        #time.sleep(1)
        pages = ["/microblogging"]
        pages_exclude = ["/terms_of_use", "/data_privacy", "/imprint", "/about"]
        done = [""]
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
                    if (link != "#") and (link != " ") and not ("http:" in link) and not ("https:" in link) and \
                            not (link in pages) and not (link in done) and not (link in pages_exclude) and \
                            not ("static" in link) and not ("{{" in link):
                        pages.append(link)
