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
import functools
import json
from smtplib import SMTPException
from django.http import HttpResponse
from node_storage.structure_parser import InvalidWikiStructure


def json_error_response(identifier, *args):
    response = {'errorResponse': {
        'errorID': identifier,
        'additionalInfo': args,
    }}
    return HttpResponse(json.dumps(response),
                        content_type='application/json',
                        status=406)


################### Custom View Exceptions #####################################
class ViewError(Exception):
    """
    Base class for all custom view exceptions.
    Holds an identifier that should start with a single underscore that will get
    internationalized in the frontend.
    """
    def __init__(self, identifier, *args):
        super(Exception, self).__init__(identifier)
        self.identifier = identifier
        self.additional_info = args


UnknownNode = functools.partial(ViewError, '_UnknownNode')
UnknownUser = functools.partial(ViewError, '_UnknownUser')
UnknownEmailAddress = functools.partial(ViewError, '_UnknownEmailAddress')
MissingPOSTParameter = functools.partial(ViewError, '_MissingPOSTParameter')
IllegalPath = functools.partial(ViewError, '_IllegalPath')
EmptyText = functools.partial(ViewError, '_EmptyText')
NotAuthenticated = functools.partial(ViewError, '_NotAuthenticated')
PermissionDenied = functools.partial(ViewError, '_PermissionDenied')
DisabledAccount = functools.partial(ViewError, '_DisabledAccount')
UsernameNotAvailable = functools.partial(ViewError, '_UsernameNotAvailable')
EmailAddressNotAvailiable = functools.partial(ViewError,
                                              '_EmailAddressNotAvailiable')
InvalidUsername = functools.partial(ViewError, '_InvalidUsername')
InvalidLogin = functools.partial(ViewError, '_InvalidLogin')
InvalidEmailAddress = functools.partial(ViewError, '_InvalidEmailAddress')
InvalidActivationKey = functools.partial(ViewError, '_InvalidActivationKey')
InvalidRecoveryKey = functools.partial(ViewError, '_InvalidRecoveryKey')
InvalidURL = functools.partial(ViewError, '_InvalidURL')
InvalidMicrobloggingOptions = functools.partial(ViewError,
                                                '_InvalidMircobloggingOptions')
InvalidShortTitle = functools.partial(ViewError, '_InvalidShortTitle')


################### ErrorHandling Decorator ####################################
def ViewErrorHandling(f):
    """
    This decorator is meant to decorate views, and will catch any ViewError
    exception and return a corresponding json error response.
    It also translates InvalidWikiStructure exceptions from the backend and
    SMTPExceptions from the server to adequate json error responses.
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ViewError as e:
            return json_error_response(e.identifier, *e.additional_info)
        except InvalidWikiStructure as e:
            return json_error_response('_InvalidWikiStructure', e.args[0])
        except SMTPException as e:
            return json_error_response('_ServerError', 'SMTPError', e.args[0])

    return wrapped