#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# #############################################################################
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
# #############################################################################
#
# #############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from findeco.jsonvalidator import (
    JSONValidator, JSONValidationError, json_decode)


USERNAME = r'(?P<name>[a-zA-Z][a-zA-Z0-9-_]{0,19})'
RSSKEY = r'(?P<rsskey>[a-zA-Z0-9]{16})'

# ################ JSON Schemas ###############################################
# The JSON responses are validated by example

integer = 1
string = 'string'
boolean = True

schema = dict()

schema['user'] = {
    'displayName': string
}
schema['userInfo'] = {
    'displayName': string,
    'description': string
}
schema['userSettings'] = {
    'blockedUsers': [schema['user'], None],
    'userRights': integer,
    'followers': [schema['user'], None],
    'followees': [schema['user'], None],
    'email': string,
    'rsskey': string,
    'emailChangeRequested': integer,
    'wantsMailNotification': boolean,
    'helpEnabled': boolean,
    'preferredLanguage': string,
}
schema['authorGroup'] = [schema['userInfo']]
schema['originGroup'] = ["path", None]
schema['graphDataNode'] = {
    'path': string,
    'authorGroup': schema['authorGroup'],
    'follows': integer,
    'spamFlags': integer,
    'unFollows': integer,
    'newFollows': integer,
    'title': string,
    'originGroup': schema['originGroup']
}
schema['indexNode'] = {
    'shortTitle': string,
    'fullTitle': string,
    'index': integer,
    'authorGroup': schema['authorGroup']
}
schema['argumentIndexNode'] = {
    'argType': string,
    'fullTitle': string,
    'text': string,
    'index': integer,
    'isFollowing': integer,
    'followingCount': integer,
    'isFlagging': integer,
    'authorGroup': schema['authorGroup']
}
schema['textNode'] = {
    'wikiText': string,
    'path': string,
    'isFollowing': integer,
    'isFlagging': integer,
    'authorGroup': schema['authorGroup']
}
schema['argumentNewsNode'] = {
    'text': string,
    'fullTitle': string,
    'path': string,
    'isFollowing': integer,
    'followingCount': integer,
    'isFlagging': integer,
    'flaggingCount': integer,
    'authorGroup': schema['authorGroup'],
    'type': string
}
schema['argumentNewsCard'] = {
    'argument': schema['argumentNewsNode'],
    'node': schema['argumentNewsNode']
}
schema['loadGraphDataResponse'] = {
    'loadGraphDataResponse': {
        'graphDataChildren': [schema['graphDataNode']],
        'graphDataRelated': [schema['graphDataNode'], None]
    }
}
schema['loadIndexResponse'] = {
    'loadIndexResponse': [schema['indexNode'], None]
}
schema['loadNodeResponse'] = {
    'loadNodeResponse': {
        'fullTitle': string,
        'nodeID': integer,
        'isFollowing': integer,
        'isFlagging': integer,
        'wikiText': string,
        'authors': [string, None],
        'indexList': [schema['indexNode'], None]
    }
}
schema['loadArgumentIndexResponse'] = {
    'loadArgumentIndexResponse': [schema['argumentIndexNode'], None]
}
schema['loadTextResponse'] = {
    'loadTextResponse': {
        'paragraphs': [schema['textNode']],
        'isFollowing': integer,
        'isFlagging': integer
    }
}
schema['loadArgumentNewsResponse'] = {
    'loadArgumentNewsResponse': [schema['argumentNewsCard'], None]
}
schema['loadUserInfoResponse'] = {
    'loadUserInfoResponse': {
        'userInfo': schema['userInfo']
    }
}
schema['loadUserSettingsResponse'] = {
    'loadUserSettingsResponse': {
        'userInfo': schema['userInfo'],
        'userSettings': schema['userSettings']
    }
}
schema['loginResponse'] = {
    'loginResponse': {
        'userInfo': schema['userInfo'],
        'userSettings': schema['userSettings']
    }
}
schema['logoutResponse'] = {
    'logoutResponse': {
        'farewellMessage': string
    }
}
schema['changePasswordResponse'] = {
    'changePasswordResponse': {
    }
}
schema['deleteUserResponse'] = {
    'deleteUserResponse': {
    }
}
schema['markNodeResponse'] = {
    'markNodeResponse': {
    }
}
schema['storeSettingsResponse'] = {
    'storeSettingsResponse': {
    }
}
schema['storeTextResponse'] = {
    'storeTextResponse': {
        'path': "path"
    }
}
schema['storeProposalResponse'] = {
    'storeProposalResponse': {
        'path': "path"
    }
}
schema['storeRefinementResponse'] = {
    'storeRefinementResponse': {
        'path': "path"
    }
}
schema['storeArgumentResponse'] = {
    'storeArgumentResponse': {
        'path': "path"
    }
}
schema['errorResponse'] = {
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
    "_EmailAddressNotAvailable",
    "_InvalidUsername",
    "_InvalidLogin",
    "_InvalidEmailAddress",
    "_InvalidActivationKey",
    "_InvalidURL",
    "_InvalidMircobloggingOptions",
    "_ServerError"
]

validators = {name: JSONValidator(s) for name, s in schema.items()}


# #############################################################################
class ErrorResponseValidator(object):
    def __init__(self):
        self.validator = validators['errorResponse']

    def validate(self, data):
        self.validator.validate(data)
        if not data['errorResponse']['errorID'] in ERROR_LIST:
            raise JSONValidationError('Invalid errorID "%s"' %
                                      data['errorResponse']['errorID'])

errorResponseValidator = ErrorResponseValidator()

view_validators = {
    'load_graph_data': validators['loadGraphDataResponse'],
    'load_index': validators['loadIndexResponse'],
    'load_argument_index': validators['loadArgumentIndexResponse'],
    'load_text': validators['loadTextResponse'],
    'load_argument_news': validators['loadArgumentNewsResponse'],
    'load_node': validators['loadNodeResponse'],
    'load_user_info': validators['loadUserInfoResponse'],
    'load_user_settings': validators['loadUserSettingsResponse'],
    'login': validators['loginResponse'],
    'logout': validators['logoutResponse'],
    'change_password': validators['changePasswordResponse'],
    'delete_user': validators['deleteUserResponse'],
    'flag_node': validators['markNodeResponse'],
    'unflag_node': validators['markNodeResponse'],
    'mark_node_follow': validators['markNodeResponse'],
    'mark_node_unfollow': validators['markNodeResponse'],
    'store_settings': validators['storeSettingsResponse'],
    'store_proposal': validators['storeProposalResponse'],
    'store_refinement': validators['storeRefinementResponse'],
    'store_argument': validators['storeArgumentResponse']
}


def validate_response(response, view):
    response = json_decode(response)
    if 'errorResponse' in response:
        errorResponseValidator.validate(response)
        return False
    validator = view_validators[view]
    validator.validate(response)
    return True
