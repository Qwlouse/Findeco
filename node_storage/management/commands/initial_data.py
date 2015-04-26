#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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

import django
from django.core.management import BaseCommand
from django.db import transaction
from findeco.paths import SHORT_TITLE
from findeco.project_path import project_path
from node_storage.factory import create_user, create_slot
from node_storage.path_helpers import get_root_node
from node_storage.structure_parser import parse, create_structure_from_structure_node_schema
import re
import os

comment_line_pattern = re.compile(r"^\s*#")


if django.VERSION < (1, 6, 0, '', 0):
    atomic = transaction.commit_on_success
else:
    atomic = transaction.atomic


@atomic
def create_initial_data():
    root = get_root_node()
    decided = create_user("Beschluss_Programm",
                          description="Diese Vorschläge wurden in ihrer urspünglichen "
                                      "Fassung schon von einem Parteitag beschlossen. "
                                      "Weiterentwicklungen dieser Vorschläge sind "
                                      "natürlich kein beschlossenes Programm.",
                          groups=['texters', 'voters', 'bloggers'])

    with open(project_path("initial_data/root.txt"), 'r') as f:
        lines = f.readlines()
        for l in lines:
            if comment_line_pattern.match(l):
                continue

            slot_name, src_file = l.split()
            assert re.match('^' + SHORT_TITLE + '$', slot_name), \
                "Invalid short title '%s'." % slot_name

            src_path = project_path(os.path.join('initial_data', src_file))
            assert os.path.exists(src_path), \
                "Source file not found: '%s'." % src_path

            print("Creating '%s' from file '%s'." % (slot_name, src_path))
            slot = create_slot(slot_name)
            root.append_child(slot)
            with open(src_path, 'r') as src:
                schema = parse(unicode(src.read(), encoding='utf-8'), slot.title)
                create_structure_from_structure_node_schema(schema, slot, decided)


class Command(BaseCommand):
    args = ''
    help = 'Creates initial data to populate the database'

    def handle(self, *args, **options):
        self.stdout.write("Creating initial data ...\n")
        create_initial_data()
