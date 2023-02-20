# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import datetime


def asset_columns_generator(fields: dict):
    _fields = []
    for key, value in fields.items():
        if isinstance(value, str) or isinstance(value, bool):
            _type = 'str'
        elif isinstance(value, int):
            _type = 'int'
        elif isinstance(value, dict) or isinstance(value, list):
            _type = 'dict'
        elif isinstance(value, datetime.date):
            _type = 'date'
        elif isinstance(value, datetime.datetime):
            _type = 'datetime'
        elif isinstance(value, float):
            _type = 'float'
        else:
            raise Exception(f'不支持的类型, value: {value}')
        _fields.append({'name': key, 'type': _type})
    return _fields


