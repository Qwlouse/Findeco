#!/usr/bin/env python3
# coding=utf-8
# region License
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
#endregion #####################################################################

from node_storage.models import Node, Vote, SpamFlag, Argument, Text, NodeOrder, TextCache
from node_storage.models import IndexCache
from node_storage.path_helpers import get_node_for_path, get_favorite_if_slot
from node_storage.path_helpers import get_ordered_children_for
from node_storage.path_helpers import IllegalPath, get_root_node
from node_storage.structure_parser import parse, create_structure_from_structure_node_schema
from node_storage.structure_parser import get_title_from_text, split_title_from_text
from node_storage.structure_parser import create_derivate_from_structure_node_schema