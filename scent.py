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

from sniffer.api import file_validator, runnable
import os
import termstyle

# you can customize the pass/fail colors like this
pass_fg_color = termstyle.green
pass_bg_color = termstyle.bg_default
fail_fg_color = termstyle.red
fail_bg_color = termstyle.bg_default


# this gets invoked on every file that gets changed in the directory. Return
# True to invoke any runnable functions, False otherwise.
@file_validator
def py_files(filename):
    ## This is a hack to also catch changes done with Pycharm and Gedit
    ## I have no idea why they don't show up on themselves, but the version
    ## with '~' or '___jb_bak___' prepended shows up, so ....
    filename = filename.strip('~').strip('___jb_bak___')
    return filename.endswith('.py') and \
        not os.path.basename(filename).startswith('.')


@runnable
def execute_manage_test(*args):
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'findeco.settings'
    exit_code = os.system('./manage.py test --attr="!selenium"' + " ".join(args[1:]))
    return exit_code == 0