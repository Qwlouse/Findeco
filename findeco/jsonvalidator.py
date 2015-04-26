"""
Validates Json API Calls 

Software License Agreement (BSD License)

Copyright (c) 2007, Maxim Derkachev.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
  * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
  * Neither the name of the Maxim Derkachev nor the names of its contributors
    may be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

* JSON schema data validation.
* Author: Maxim Derkachev (max.derkachev@gmail.com)
* http://code.google.com/p/jsonvalidator/
*
Schema is a JSON-compatible string or Python object, is an example of a valid
data structure.
Example schemas:
*   '["string", "number"]'
    '["anything", 1]'
    Valid for [], [3], [""], ["something", 4, "foo"]
    Invalid for {}, 1, "", [true], [1, false]

*   {"one": 1, "two": {"three":"string?"}}
    Valid for {"one":0, "two":{}}, {"one":0, "two":{"three":"something"}},
              {"one":2, "two":{"three":""}}
    Invalid for 1, "", [], {}, {"one":0}, {"one":0, "two":{"three":1}},
              {"one":0, "two":{}, "foo":"bar"}

The following schemas are equivalent:
1. {"a":"there can be a string"}, {"a": "string"}, {"a": ""}
2. {"b":4563}, {"b": 0}, {"b": "number"}

Value types can be defined as:
*  literals of that type, e.g. {} for object, [] for array,
   1 for number, "anything" for string, null for null,
   false or true for boolean;
* "string" for string, "number" for number, "bool" for boolean.
   In this case you can add "?" to indicate that the value can be undefined or
   null. E.g. "number?" is matched by numbers, undefined values and nulls


* API:
# JSON string
schema = '["string", "number"]'
# or an object:
schema = ["any string", 1]
validator = JSONValidator(schema)
isValid = validator.validate(data) # data is a Python object  or a JSON string

Raise JSONError on invalid JSON (that can not be parsed), or JSONValidationError
(no JSON parse errors, but invalid for the schema specified)
"""

import json
import types


class JSONValidationError(Exception):
    pass


class JSONError(Exception):
    pass


class BaseHandler(object):
    def __init__(self, schema, required):
        self.required = required

    def __call__(self, data):
        return self.validate(data)

    def validate(self, data):
        if data is None and self.required:
            raise JSONValidationError("Required field is missing")
        return data


class StringHandler(BaseHandler):
    def validate(self, data):
        data = super(StringHandler, self).validate(data)
        if data and not isinstance(data, str):
            raise JSONValidationError("data is not a string: %s" % str(data))
        return data


class NumberHandler(BaseHandler):
    def validate(self, data):
        data = super(NumberHandler, self).validate(data)
        if data and not isinstance(data, (int, float)):
            raise JSONValidationError("data is not a number: %s" % str(data))
        return data


class BooleanHandler(BaseHandler):
    def validate(self, data):
        data = super(BooleanHandler, self).validate(data)
        if data is not None and not isinstance(data, bool):
            raise JSONValidationError("data is not a boolean: %s" % str(data))
        return data


class NullHandler(BaseHandler):
    def validate(self, data):
        if data is not None:
            raise JSONValidationError("data is not null: %s" % str(data))
        return data


class ObjectHandler(BaseHandler):
    def __init__(self, schema, required):
        super(ObjectHandler, self).__init__(schema, required)
        self.handlers = {}
        self.validKeys = set()
        for key, value in schema.items():
            _type, handler = getValidator(value)
            self.handlers[key] = handler
            self.validKeys.add(key)

    def validate(self, data):
        data = super(ObjectHandler, self).validate(data)
        if not isinstance(data, dict):
            raise JSONValidationError("data is not an object: %s" % str(data))
        handlers = self.handlers
        for key, handler in handlers.items():
            keyData = data.get(key, None)
            try:
                keydata = handler(keyData)
            except JSONValidationError as e:
                raise JSONValidationError("(%s)" % key + e.message)
        if self.validKeys:
            for key in data:
                if not key in self.validKeys:
                    raise JSONValidationError("invalid object key: %s" % key)
        return data


class ArrayHandler(BaseHandler):
    def __init__(self, schema, required):
        super(ArrayHandler, self).__init__(schema, required)
        self.handlers = {}
        for value in schema:
            _type, handler = getValidator(value)
            self.handlers[_type] = handler

    def validate(self, data):
        data = super(ArrayHandler, self).validate(data)
        if not isinstance(data, list):
            raise JSONValidationError("data is not an array")
        if self.handlers and not self.handlers.get(type(None),
                                                   False) and not data:
            raise JSONValidationError("this array should not be empty")
        for value in data:
            handler = self.handlers.get(type(value), None)
            if not handler:
                raise JSONValidationError(
                    "invalid data member in array: %s" % str(value))
            value = handler(value)
        return data


HANDLERS_BY_TYPE = {str: StringHandler,
                    int: NumberHandler,
                    float: NumberHandler,
                    dict: ObjectHandler,
                    list: ArrayHandler,
                    bool: BooleanHandler,
                    type(None): NullHandler}


def getValidator(schema):
    required = True
    _type = type(schema)
    if _type is str:
        if schema.startswith("number"):
            _type = int
        elif schema.startswith("bool"):
            _type = bool
        required = not schema.endswith('?')
    handler = HANDLERS_BY_TYPE.get(_type, None)
    if handler:
        return _type, handler(schema, required)
    else:
        raise JSONError("Unsupported JSON type in schema")


class JSONValidator(object):
    validator = None

    def __init__(self, schema):
        if isinstance(schema, str):
            schema = json.loads(schema)
        _type, self.validator = getValidator(schema)

    def validate(self, data):
        if self.validator:
            if isinstance(data, str):
                parsedData = json.loads(data)
                data = parsedData
            return self.validator(data)
