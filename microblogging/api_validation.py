#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>
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
###############################################################################
#
###############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from findeco.api_validation import string, integer, JSONValidator
from findeco.api_validation import errorResponseValidator
import json

microblogNode_schema = {
    'microblogText': string,
    'authorGroup': ["user"],
    'microblogTime': integer,
    'microblogID': integer,
    'location': integer,
    'locationPath': string
}
loadMicrobloggingResponse_schema = {
    'loadMicrobloggingResponse': [microblogNode_schema, None]
}
storeMicroblogPostResponse_schema = {
    'storeMicroblogPostResponse': {
    }
}


loadMicrobloggingResponseValidator = JSONValidator(
    loadMicrobloggingResponse_schema)

storeMicroblogPostResponseValidator = JSONValidator(
    storeMicroblogPostResponse_schema)

view_validators = {
    'load_microblogging': loadMicrobloggingResponseValidator,
    'store_microblog_post': storeMicroblogPostResponseValidator,
}


def validate_response(response, view):
    response = json.loads(response)
    if 'errorResponse' in response:
        errorResponseValidator.validate(response)
        return False
    validator = view_validators[view]
    validator.validate(response)
    return True
