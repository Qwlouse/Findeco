#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
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
################################################################################
from __future__ import division, print_function, unicode_literals
from test_activation_models import ActivationTest, EmailActivationTest
from test_activation_models import PasswordRecoveryTest
from test_profile import UserProfileTest
from test_path import PathRegExTest
from test_url_resolution import UrlResolutionTest
from test_views import ViewTest
from test_view_helpers import CreateIndexNodeForSlotTest
from test_view_helpers import CreateIndexNodeForArgumentTest
from test_view_helpers import CreateUsersInfoTest, CreateUserSettingsTest
from test_view_helpers import CreateGraphDataNodeForStructureNodeTest
from test_view_helpers import StoreStructureNodeTest, StoreArgumentTest
from test_view_helpers import StoreDerivateTest
from test_view_helpers import GetIsFollowingTest, CheckUsernameSanityTest
from test_load_index import LoadIndexTest, LoadArgumentIndexTest
from test_load_node import LoadNodeTest
from test_load_text import LoadTextTest
from test_user_api import LoadUserInfoTest, LoadUserSettingsTest
from test_user_api import StoreSettingsTest, ChangePasswordTest, DeleteUserTest
from test_store_text import StoreTextTest
from test_load_graph_data import LoadGraphDataTest
from test_marking import UnFollowTest, FollowTest, MarkSpamTest, UnMarkSpamTest
from test_search import SearchTest
# from test_fe_page_start import *
# from test_fe_page_registration import *
# from test_fe_page_login import *
# from test_fe_page_profile import *
try:
    from microblogging.tests import *
except ImportError:
    pass

try:
    from node_storage.tests import *
except ImportError:
    pass



