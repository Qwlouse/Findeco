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
import json
from findeco.jsonvalidator import JSONValidator, JSONValidationError


USERNAME = r'(?P<name>[a-zA-Z][a-zA-Z0-9-_]{0,19})'
RSSKEY = r'(?P<rsskey>[a-zA-Z0-9]{16})'

################# JSON Schemas #################################################
# The JSON responses are validated by example

integer = 1
string = "string"
boolean = True
user_schema = {
    'displayName': string
}
userInfo_schema = {
    'displayName': string,
    'description': string
}
userSettings_schema = {
    'blockedUsers': [user_schema, None],
    'userRights': integer,
    'followers': [user_schema, None],
    'followees': [user_schema, None],
    'email': string,
    'rsskey': string,
    'emailChangeRequested': integer,
    'wantsMailNotification': boolean,
    'helpEnabled': boolean
}
authorGroup_schema = [userInfo_schema]
originGroup_schema = ["path", None]
graphDataNode_schema = {
    'path': string,
    'authorGroup': authorGroup_schema,
    'follows': integer,
    'spamFlags': integer,
    'unFollows': integer,
    'newFollows': integer,
    'title': string,
    'originGroup': originGroup_schema
}
indexNode_schema = {
    'shortTitle': string,
    'fullTitle': string,
    'index': integer,
    'authorGroup': authorGroup_schema
}
argumentIndexNode_schema = {
    'argType': string,
    'fullTitle': string,
    'text': string,
    'index': integer,
    'isFollowing': integer,
    'followingCount': integer,
    'isFlagging': integer,
    'authorGroup': authorGroup_schema
}
textNode_schema = {
    'wikiText': string,
    'path': string,
    'isFollowing': integer,
    'isFlagging': integer,
    'authorGroup': authorGroup_schema
}
argumentNewsNode_schema = {
    'text': string,
    'fullTitle': string,
    'path': string,
    'isFollowing': integer,
    'followingCount': integer,
    'isFlagging': integer,
    'flaggingCount': integer,
    'authorGroup': authorGroup_schema,
    'type': string
}
argumentNewsCard_schema = {
    'argument': argumentNewsNode_schema,
    'node': argumentNewsNode_schema
}
loadGraphDataResponse_schema = {
    'loadGraphDataResponse': {
        'graphDataChildren': [graphDataNode_schema],
        'graphDataRelated': [graphDataNode_schema, None]
    }
}
loadIndexResponse_schema = {
    'loadIndexResponse': [indexNode_schema, None]
}
loadNodeResponse_schema = {
    'loadNodeResponse': {
        'fullTitle': string,
        'nodeID': integer,
        'isFollowing': integer,
        'isFlagging': integer,
        'wikiText': string,
        'authors': [string, None],
        'indexList': [indexNode_schema, None]
    }
}
loadArgumentIndexResponse_schema = {
    'loadArgumentIndexResponse': [argumentIndexNode_schema, None]
}
loadTextResponse_schema = {
    'loadTextResponse': {
        'paragraphs': [textNode_schema],
        'isFollowing': integer,
        'isFlagging': integer
    }
}
loadArgumentNewsResponse_schema = {
    'loadArgumentNewsResponse': [argumentNewsCard_schema, None]
}
loadUserInfoResponse_schema = {
    'loadUserInfoResponse': {
        'userInfo': userInfo_schema
    }
}
loadUserSettingsResponse_schema = {
    'loadUserSettingsResponse': {
        'userInfo': userInfo_schema,
        'userSettings': userSettings_schema
    }
}
loginResponse_schema = {
    'loginResponse': {
        'userInfo': userInfo_schema,
        'userSettings': userSettings_schema
    }
}
logoutResponse_schema = {
    'logoutResponse': {
        'farewellMessage': string
    }
}
changePassword_schema = {
    'changePasswordResponse': {
    }
}
deleteUser_schema = {
    'deleteUserResponse': {
    }
}
markNodeResponse_schema = {
    'markNodeResponse': {
    }
}
storeSettingsResponse_schema = {
    'storeSettingsResponse': {
    }
}
storeTextResponse_schema = {
    'storeTextResponse': {
        'path': "path"
    }
}
errorResponse_schema = {
    'errorResponse': {
        'errorID': string,
        'additionalInfo': [string, None]
    }
}

ERROR_LIST = [
    "_UnknownNode",
    "_UnknownUser",
    "_UnknownEmailAddress",
    "_MissingPOSTParameter",
    "_IllegalPath",
    "_NotAuthenticated",
    "_PermissionDenied",
    "_DisabledAccount",
    "_UsernameNotAvailable",
    "_EmailAddressNotAvailiable",
    "_InvalidUsername",
    "_InvalidLogin",
    "_InvalidEmailAddress",
    "_InvalidActivationKey",
    "_InvalidURL",
    "_InvalidMircobloggingOptions",
    "_ServerError"
]


################################################################################

userInfoValidator = JSONValidator(userInfo_schema)
userSettingsValidator = JSONValidator(userSettings_schema)
indexNodeValidator = JSONValidator(indexNode_schema)
argumentIndexNodeValidator = JSONValidator(argumentIndexNode_schema)
loadGraphDataResponseValidator = JSONValidator(loadGraphDataResponse_schema)
loadIndexResponseValidator = JSONValidator(loadIndexResponse_schema)
loadNodeResponseValidator = JSONValidator(loadNodeResponse_schema)
loadArgumentIndexResponseValidator = JSONValidator(
    loadArgumentIndexResponse_schema)
loadTextResponseValidator = JSONValidator(loadTextResponse_schema)
loadArgumentNewsResponseValidator = JSONValidator(loadArgumentNewsResponse_schema)
loadUserInfoResponseValidator = JSONValidator(loadUserInfoResponse_schema)
loadUserSettingsResponseValidator = JSONValidator(
    loadUserSettingsResponse_schema)
loginResponseValidator = JSONValidator(loginResponse_schema)
logoutResponseValidator = JSONValidator(logoutResponse_schema)
changePasswordValidator = JSONValidator(changePassword_schema)
deleteUserValidator = JSONValidator(deleteUser_schema)
markNodeResponseValidator = JSONValidator(markNodeResponse_schema)
storeSettingsResponseValidator = JSONValidator(storeSettingsResponse_schema)
storeTextResponseValidator = JSONValidator(storeTextResponse_schema)


class ErrorResponseValidator(object):
    def __init__(self):
        self.validator = JSONValidator(errorResponse_schema)

    def validate(self, data):
        self.validator.validate(data)
        if not data['errorResponse']['errorID'] in ERROR_LIST:
            raise JSONValidationError('Invalid errorID "%s"' %
                                      data['errorResponse']['errorID'])

errorResponseValidator = ErrorResponseValidator()

view_validators = {
    'load_graph_data': loadGraphDataResponseValidator,
    'load_index': loadIndexResponseValidator,
    'load_argument_index': loadArgumentIndexResponseValidator,
    'load_text': loadTextResponseValidator,
    'load_argument_news': loadArgumentNewsResponseValidator,
    'load_node': loadNodeResponseValidator,
    'load_user_info': loadUserInfoResponseValidator,
    'load_user_settings': loadUserSettingsResponseValidator,
    'login': loginResponseValidator,
    'logout': logoutResponseValidator,
    'change_password': changePasswordValidator,
    'delete_user': deleteUserValidator,
    'flag_node': markNodeResponseValidator,
    'unflag_node': markNodeResponseValidator,
    'mark_node_follow': markNodeResponseValidator,
    'mark_node_unfollow': markNodeResponseValidator,
    'store_settings': storeSettingsResponseValidator,
    'store_text': storeTextResponseValidator
}


def validate_response(response, view):
    response = json.loads(response)
    if 'errorResponse' in response:
        errorResponseValidator.validate(response)
        return False
    validator = view_validators[view]
    validator.validate(response)
    return True
