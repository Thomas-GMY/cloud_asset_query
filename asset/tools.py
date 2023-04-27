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


if __name__ == '__main__':

    fields_demo = {
    "id" : "a253be25-ae7c-4013-978b-3c0785eccd63",
    "router_id" : "b1d81744-5165-48b8-916e-e56626feb88f",
    "status" : "ACTIVE",
    "description" : "nat01",
    "admin_state_up" : 'true',
    "tenant_id" : "27e25061336f4af590faeabeb7fcd9a3",
    "created_at" : "2017-11-15 14:50:39.505112",
    "spec" : "2",
    "internal_network_id" : "5930796a-6026-4d8b-8790-6c6bfc9f87e8",
    "name" : "wj3",
    "enterprise_project_id" : "0aad99bc-f5f6-4f78-8404-c598d76b0ed2"
  }
    for asset in asset_columns_generator(fields=fields_demo):
        print(str(asset) + ',')