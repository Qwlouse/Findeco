#!/usr/bin/python
# coding=utf-8
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

from django.db import transaction
from node_storage.factory import create_slot, create_user
from node_storage.path_helpers import get_root_node
from node_storage.structure_parser import parse, create_structure_from_structure_node_schema

@transaction.commit_on_success
def createInitialData():
    root = get_root_node()
    decided = create_user("Beschlossenes Programm")

    # Grundsatzprogramm Bundesweit
    grundsatzprogramm = create_slot("Grundsatzprogramm")
    root.append_child(grundsatzprogramm)
    with open("initial_data/grundsatzprogramm_bund.txt", 'r') as f:
        gsp_text = f.read()
    schema = parse(unicode(gsp_text, encoding='utf-8'),grundsatzprogramm.title)
    create_structure_from_structure_node_schema(schema, grundsatzprogramm, [decided])

    # Wahlprogramm BTW
    wahlprogramm_btw = create_slot("Wahlprogramm_BTW")
    root.append_child(wahlprogramm_btw)
    with open("initial_data/wahlprogramm_btw.txt", 'r') as f:
        wpbtw_text = f.read()
    schema = parse(unicode(wpbtw_text, encoding='utf-8'),wahlprogramm_btw.title)
    create_structure_from_structure_node_schema(schema, wahlprogramm_btw, [decided])

    # Positionspapiere Bund
    posp_bund = create_slot("Positionspapiere")
    root.append_child(posp_bund)
    with open("initial_data/positionspapiere_bund.txt", 'r') as f:
        pospbund_text = f.read()
    schema = parse(unicode(pospbund_text, encoding='utf-8'),posp_bund.title)
    create_structure_from_structure_node_schema(schema, posp_bund, [decided])