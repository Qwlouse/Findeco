#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, print_function, unicode_literals
from django.contrib import admin
from models import Node, Argument, Text, Vote, NodeOrder, ArgumentOrder, Derivation

class TextInline(admin.StackedInline):
    model = Text
    max_num = 1
    can_delete = True

class ChildInline(admin.TabularInline):
    model = NodeOrder
    extra = 1
    fk_name = "parent"

class ParentInline(admin.TabularInline):
    model = NodeOrder
    extra = 1
    fk_name = "child"

class ArgumentInline(admin.TabularInline):
    model = ArgumentOrder
    extra = 1
    fk_name = "node"

class ArgNodeInline(admin.TabularInline):
    model = ArgumentOrder
    extra = 1
    fk_name = "argument"


class DerivationInline(admin.TabularInline):
    model = Derivation
    extra = 1
    fk_name = "source"

class ArgumentAdmin(admin.ModelAdmin):
    model = Argument
    list_display = ('title', 'id', 'arg_type', 'node_type')
    inlines = [TextInline, ArgNodeInline]

class NodeAdmin(admin.ModelAdmin):
    model = Node
    list_display = ('get_a_path', 'title', 'get_follows', 'id', 'node_type')
    inlines = [ParentInline, ChildInline, TextInline, ArgumentInline, DerivationInline]

class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ('id', 'user', 'head')
    list_display_links = ('head',)

admin.site.register(Node, NodeAdmin)
admin.site.register(Argument, ArgumentAdmin)
admin.site.register(Vote, VoteAdmin)
