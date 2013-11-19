#!/usr/bin/python
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

from __future__ import division, print_function, unicode_literals

import os
import re

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from findeco.paths import SHORT_TITLE
from findeco.project_path import project_path
from node_storage import get_root_node, parse
from node_storage import create_structure_from_structure_node_schema
from node_storage.factory import create_slot


@transaction.commit_on_success
def create_topic(src_path, topic_name):
        print("Creating '%s' from file '%s'." % (topic_name, src_path))
        root = get_root_node()
        decided = User.objects.get(username="Beschlossenes Programm")
        slot = create_slot(topic_name)
        root.append_child(slot)
        with open(src_path, 'r') as src:
            schema = parse(unicode(src.read(), encoding='utf-8'), slot.title)
            create_structure_from_structure_node_schema(schema, slot, decided)


class Command(BaseCommand):
    args = '<TopicName> <InitalTextFilename>'
    help = 'Add a new topic to the root node. It will have the path ' \
           '/TopicName.1 and the content of <InitialTextFile> will be parsed ' \
           'and used to populate this topic.\n ' \
           'BE CAREFUL: This operation cannot be undone! Backup your Database!'

    def handle(self, *args, **options):
        if len(args) < 2:
            print("You have to provide a <TopicName> and a "
                  "<InitalTextFilename>!")

        if len(args) > 2:
            print("Please provide exactly two arguments!")

        topic_name = args[0]
        assert re.match(SHORT_TITLE, topic_name), \
            "Invalid topic name '%s'. Topic name should be only alphanumeric " \
            "chars up to a length of 20." % topic_name

        filename = args[1]
        src_path = project_path(filename)
        if not os.path.exists(src_path):
            print("File '%s' does not exist!" % src_path)

        create_topic(src_path, topic_name)