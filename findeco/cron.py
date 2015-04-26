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

from datetime import datetime
from findeco.models import Activation, PasswordRecovery


from django_cron import CronJobBase, Schedule


class ActivationKeyPruning(CronJobBase):
    RUN_EVERY_MINS = 60  # every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'findeco.activation_key_pruning'    # a unique code

    def do(self):
        now = datetime.now()
        for act in Activation.objects.filter(key_valid_until__lt=now):
            act.user.delete()
            act.delete()
        PasswordRecovery.objects.filter(key_valid_until__lt=now).delete()
