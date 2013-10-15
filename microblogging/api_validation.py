#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from findeco.api_validation import string, integer, JSONValidator
from findeco.api_validation import errorResponseValidator
import json

microblogNode_schema = {
    'microblogText': string,
    'authorGroup': ["user"],
    'microblogTime': integer,
    'microblogID': integer
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