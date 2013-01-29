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
from django.core.management import BaseCommand
from django.db import transaction
from node_storage import get_node_for_path
from node_storage.factory import create_user, create_slot, create_structureNode, create_argument, create_vote, create_spam_flag
from node_storage.path_helpers import get_root_node
from node_storage.structure_parser import parse, create_structure_from_structure_node_schema

def create_alternatives_for_urheberrecht(path):
    ulf = create_user('ulf')
    timo = create_user('timo')
    slot_path = path.rsplit('.',1)[0]
    slot = get_node_for_path(slot_path)

    w1 = "Reform des Urheberrechts sollte von der Basis kommen."

    a1 = create_structureNode("Urheberrecht", w1, authors=[ulf])
    slot.append_child(a1)


    w2a = "Abschaffung des Urheberrechts!"
    a2a = create_structureNode("Kein Urheberrecht", w2a, authors=[ulf])
    slot.append_child(a2a)

    w2b = "Völlige Abschaffung des Urheber- und Patentrechts!"
    a2b = create_structureNode("Kein Urheberrecht", w2b, authors=[ulf])
    slot.append_child(a2b)
    arga = create_argument('con',
        "Patentrecht ist genauso böse",
        "Das patentrecht ist mindestens genauso schlimm und muss auch weg!",
        [ulf])
    a2a.add_derivate(arga, a2b)

    w2c = "Völlige Abschaffung des Urheber- und Patentrechts! Außerdem Todesstrafe für alle Patentanwälte."
    a2c = create_structureNode("Kein Urheberrecht", w2c, authors=[timo])
    slot.append_child(a2c)
    argb = create_argument('con',
        "Patentanwälte stinken!",
        "Dieses Pack gehört ausgerottet!",
        [timo]
    )
    a2b.add_derivate(argb, a2c)

    # create votes
    original = get_node_for_path(path)
    hugo = create_user("hugo")
    hans = create_user("hans")
    hein = create_user("hein")
    create_vote(ulf, [a1])
    create_vote(ulf, [a2a, a2b])
    create_vote(timo, [a2c])
    create_vote(hugo, [original])
    create_vote(hein, [original])
    create_vote(hans, [a1])
    create_vote(hans, [a2b])
    create_vote(hans, [arga])
    create_vote(ulf, [arga])
    create_spam_flag(hein, [argb])
    create_spam_flag(hein, [a2c])


@transaction.commit_on_success
def create_initial_data():
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
    create_alternatives_for_urheberrecht("Wahlprogramm_BTW.1/Urheberrecht.1")

    # Positionspapiere Bund
    posp_bund = create_slot("Positionspapiere")
    root.append_child(posp_bund)
    with open("initial_data/positionspapiere_bund.txt", 'r') as f:
        pospbund_text = f.read()
    schema = parse(unicode(pospbund_text, encoding='utf-8'),posp_bund.title)
    create_structure_from_structure_node_schema(schema, posp_bund, [decided])

class Command(BaseCommand):
    args = ''
    help = 'Creates initial data to populate the database'

    def handle(self, *args, **options):
        self.stdout.write("Creating initial data ...\n")
        create_initial_data()
