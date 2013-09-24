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
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from microblogging.factory import create_post
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
    arga = a2a.add_derivate(a2b, 'con',
        "Patentrecht ist genauso böse",
        "Das patentrecht ist mindestens genauso schlimm und muss auch weg!",
        [ulf])

    w2c = "Völlige Abschaffung des Urheber- und Patentrechts! Außerdem Todesstrafe für alle Patentanwälte."
    a2c = create_structureNode("Kein Urheberrecht", w2c, authors=[timo])
    slot.append_child(a2c)
    argb = a2b.add_derivate(a2c, 'con',
        "Patentanwälte stinken!",
        "Dieses Pack gehört ausgerottet!",
        [timo])

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


def create_some_microblogging(path=None):
    if User.objects.filter(username="Blogger 1").count() > 0:
        blogger1 = User.objects.filter(username="Blogger 1").all()[0]
    else:
        blogger1 = create_user("Blogger 1")
    create_post("Meine Oma fährt im Hühnerstall Motorrad!" if not path else "Meine Oma erwähnt /" +
                path + " im Hühnerstall.", blogger1)
    if User.objects.filter(username="Troll").count() > 0:
        troll = User.objects.filter(username="Troll").all()[0]
    else:
        troll = create_user("Troll")
    if path:
        create_post("Ich erwähne /" + path + " um zu trollen. Lies das was ich schreibe und ärgere dich!",
                    troll)


@transaction.commit_on_success
def create_initial_data():
    root = get_root_node()
    decided = create_user("Beschlossenes Programm")
    #create_some_microblogging()

    # Grundsatzprogramm Bundesweit
    #grundsatzprogramm = create_slot("Grundsatzprogramm")
    #root.append_child(grundsatzprogramm)
    #with open("initial_data/grundsatzprogramm_bund.txt", 'r') as f:
    #    gsp_text = f.read()
    #schema = parse(unicode(gsp_text, encoding='utf-8'), grundsatzprogramm.title)
    #create_structure_from_structure_node_schema(schema, grundsatzprogramm, decided)
    #create_some_microblogging("Grundsatzprogramm.1")

    # Wahlprogramm BTW
    #wahlprogramm_btw = create_slot("Wahlprogramm_BTW")
    #root.append_child(wahlprogramm_btw)
    #with open("initial_data/wahlprogramm_btw.txt", 'r') as f:
    #    wpbtw_text = f.read()
    #schema = parse(unicode(wpbtw_text, encoding='utf-8'), wahlprogramm_btw.title)
    #create_structure_from_structure_node_schema(schema, wahlprogramm_btw, decided)
    #create_alternatives_for_urheberrecht("Wahlprogramm_BTW.1/Urheberrecht.1")
    #create_some_microblogging("Wahlprogramm_BTW.1/Urheberrecht.1")

    # Positionspapiere Bund
    #posp_bund = create_slot("Positionspapiere")
    #root.append_child(posp_bund)
    #with open("initial_data/positionspapiere_bund.txt", 'r') as f:
    #    pospbund_text = f.read()
    #schema = parse(unicode(pospbund_text, encoding='utf-8'), posp_bund.title)
    #create_structure_from_structure_node_schema(schema, posp_bund, decided)

    # Wahlprogramm Rheinland-Pfalz
    wahlprogramm_rlp = create_slot("Wahlprogramm_RLP")
    root.append_child(wahlprogramm_rlp)
    with open("initial_data/wahlprogramm_rlp.txt", 'r') as f:
        wahlprogrammrlp_text = f.read()
    schema = parse(unicode(wahlprogrammrlp_text, encoding='utf-8'), wahlprogramm_rlp.title)
    create_structure_from_structure_node_schema(schema, wahlprogramm_rlp, decided)

    # Positionspapiere Rheinland-Pfalz
    posp_rlp = create_slot("Positionspapiere_RLP")
    root.append_child(posp_rlp)
    with open("initial_data/positionspapiere_rlp.txt", 'r') as f:
        posprlp_text = f.read()
    schema = parse(unicode(posprlp_text, encoding='utf-8'), posp_rlp.title)
    create_structure_from_structure_node_schema(schema, posp_rlp, decided)

    # Satzung Rheinland-Pfalz
    satzung_rlp = create_slot("Satzung_RLP")
    root.append_child(satzung_rlp)
    with open("initial_data/satzung_rlp.txt", 'r') as f:
        satzungrlp_text = f.read()
    schema = parse(unicode(satzungrlp_text, encoding='utf-8'), satzung_rlp.title)
    create_structure_from_structure_node_schema(schema, satzung_rlp, decided)

    # Spielwiese
    spielwiese = create_slot("Spielwiese")
    root.append_child(spielwiese)
    with open("initial_data/spielwiese.txt", 'r') as f:
        spielwiese_text = f.read()
    schema = parse(unicode(spielwiese_text, encoding='utf-8'), spielwiese.title)
    create_structure_from_structure_node_schema(schema, spielwiese, decided)


class Command(BaseCommand):
    args = ''
    help = 'Creates initial data to populate the database'

    def handle(self, *args, **options):
        self.stdout.write("Creating initial data ...\n")
        create_initial_data()
