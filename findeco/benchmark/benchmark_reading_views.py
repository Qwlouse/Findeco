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
from timeit import timeit
from django.core.urlresolvers import reverse, resolve
from django.test.client import RequestFactory


def setup(view, kwargs):
    url = reverse(view, kwargs=kwargs)
    res = resolve(url)
    factory = RequestFactory()
    request = factory.get(url)
    f = lambda : res.func(request, **res.kwargs)
    return f


def time_view(view, kwargs):
    setup = """
from __main__ import setup
view = setup('%s', kwargs=%s)
"""
    return timeit("view()",number=100,  setup=setup%(view, kwargs.__repr__()))

if __name__ == "__main__":
    views = [
        ('load_index', dict(path='Grundsatzprogramm.1'))
    ]
    for v, kwargs in views:
        time = time_view(v, kwargs)
        print(v + " took %0.2fms per call"%(time*10))
