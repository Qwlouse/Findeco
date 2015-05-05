#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>
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
###############################################################################
#
###############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from django.core.management import BaseCommand
from node_storage.path_helpers import get_node_for_path
from node_storage.tools import delete_node


class Command(BaseCommand):
    args = '<NodePath>'
    help = 'Delete a node and all children, votes, posts, derivates, ' \
           'cache entries, arguments, and empty parents associated with it. '\
           'BE CAREFUL: This operation cannot be undone! Backup your Database!'

    def handle(self, *args, **options):
        if len(args) < 1:
            print("You have to provide a <NodePath>.")

        if len(args) > 1:
            print("Please provide exactly one argument!")

        node_path = args[0]

        node = get_node_for_path(node_path)
        assert node, "Node for path '%s' does not exist." % node_path

        delete_node(node)