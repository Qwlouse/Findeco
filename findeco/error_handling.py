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
import functools
from django.http import HttpResponse
import json
from node_storage.structure_parser import InvalidWikiStructure
from smtplib import SMTPException


def json_error_response(identifier, *args):
    response = {'errorResponse': {
        'errorID': identifier,
        'additionalInfo': args,
        }}
    return HttpResponse(json.dumps(response),
                        mimetype='application/json',
                        status=406)


class ViewError(Exception):
    def __init__(self, identifier, *args):
        super(Exception, self).__init__(identifier)
        self.identifier = identifier
        self.additional_info = args


UnknownNode = functools.partial(ViewError, 'UnknownNode')
UnknownUser = functools.partial(ViewError, 'UnknownUser')
UnknownEmailAddress = functools.partial(ViewError, 'UnknownEmailAddress')
MissingPOSTParameter = functools.partial(ViewError, 'MissingPOSTParameter')
IllegalPath = functools.partial(ViewError, 'IllegalPath')
NotAuthenticated = functools.partial(ViewError, 'NotAuthenticated')
PermissionDenied = functools.partial(ViewError, 'PermissionDenied')
DisabledAccount = functools.partial(ViewError, 'DisabledAccount')
UsernameNotAvailable = functools.partial(ViewError, 'UsernameNotAvailable')
EmailAddressNotAvailiable = functools.partial(ViewError,
                                              'EmailAddressNotAvailiable')
InvalidUsername = functools.partial(ViewError, 'InvalidUsername')
InvalidLogin = functools.partial(ViewError, 'InvalidLogin')
InvalidEmailAddress = functools.partial(ViewError, 'InvalidEmailAddress')
InvalidActivationKey = functools.partial(ViewError, 'InvalidActivationKey')
InvalidURL = functools.partial(ViewError, 'InvalidURL')


def ViewErrorHandling(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ViewError, e:
            return json_error_response(e.identifier, *e.additional_info)
        except InvalidWikiStructure, e:
            return json_error_response('InvalidWikiStructure', e.message)
        except SMTPException, e:
            return json_error_response('ServerError', 'SMTPError', e.message)

    return wrapped