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
                "AddTime": "2020-11-28 10:05:52",
                "ConsoleLogin": 0,
                "DeletionTaskId": 'null',
                "Description": "当前角色为腾讯云自动化助手 (TAT)服务相关角色，该角色将在已关联策略的权限范围内访问您的其他云服务资源。",
                "PolicyDocument": "{\"version\":\"2.0\",\"statement\":[{\"action\":\"sts:AssumeRole\",\"effect\":\"allow\",\"principal\":{\"service\":[\"command.tat.cloud.tencent.com\"]}}]}",
                "RoleId": "4611686018433460000",
                "RoleName": "TAT_QCSLinkedRoleInCommand",
                "RoleType": "service_linked",
                "SessionDuration": 43200,
                "Tags": [],
                "UpdateTime": "2020-11-28 10:05:52"
    }
    for asset in asset_columns_generator(fields=fields_demo):
        print(str(asset) + ',')