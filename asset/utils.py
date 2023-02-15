# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import re
import json
import boto3
import datetime

from tencentcloud.cam.v20190116 import cam_client, models

from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest
from aliyunsdkcore.client import AcsClient

from boto3 import client as aws_client
from typing import Tuple, Union

from asset.schema import AwsCredential, STSAssumeRoleCredential


def to_hump_underline(string) -> str:
    return re.sub(r"(?P<key>[A-Z])", r"_\g<key>", string).lower().strip('_')


def register_assets(cloud_provider):
    import importlib
    from asset.asset_register import cloud_providers

    importlib.import_module(f'asset.{cloud_provider}')
    return getattr(cloud_providers, cloud_provider)


def tencent_parser_response(response, response_filed: str) -> list:
    return json.loads(response.to_json_string())[response_filed]


def aliyun_parser_response(response, response_filed: str, child_response_filed: str = None) -> list:
    if child_response_filed:
        return json.loads(response)[response_filed][child_response_filed]
    return json.loads(response)[response_filed]


def aws_parser_response(
        response: dict, response_filed: str, child_response_filed: str = None) -> Tuple[Union[list, str, dict], str]:
    assets = response.get(response_filed)
    next_token = response.get('NextToken')
    if child_response_filed is not None:
        if isinstance(assets, list):
            _assets = []
            for asset in assets:
                _assets += asset[child_response_filed]
            return _assets, next_token
        elif isinstance(assets, dict):
            return assets.get(child_response_filed), next_token
        else:
            raise Exception('')
    return assets, next_token


def recursive_dict(_value):
    for key, value in _value.items():
        if isinstance(value, datetime.datetime):
            _value[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            _value[key] = value.strftime('%Y-%m-%d')
        elif isinstance(value, dict):
            _value[key] = recursive_dict(value)
        elif isinstance(value, list):
            _value[key] = recursive_list(value)
        elif isinstance(value, bool):
            _value[key] = str(value)
    return _value


def recursive_list(value):
    _value_list = []
    for index in range(len(value)):
        _value = value[index]
        if isinstance(_value, dict):
            _value_list.append(recursive_dict(_value))
        elif isinstance(_value, list):
            _value_list.append(recursive_list(_value))
        elif isinstance(value, bool):
            _value_list.append(str(_value))
        else:
            _value_list.append(_value)
    return _value_list


def get_tencent_account_id(cred):
    client = cam_client.CamClient(credential=cred, region=None)
    response = client.GetUserAppId(models.GetUserAppIdRequest())
    return response.OwnerUin


def get_aliyun_account_id(cred):
    request = GetCallerIdentityRequest.GetCallerIdentityRequest()
    response = AcsClient(credential=cred).do_action_with_exception(request)
    return json.loads(response)['AccountId']


def get_aws_account_id(cred: AwsCredential):
    response = aws_client('sts', **cred.dict()).get_caller_identity()
    return response['Account']


def aws_assume_role(arn, role_session_name='fetch_asset', duration_seconds=3600) -> AwsCredential:
    response = boto3.client('sts').assume_role(
        RoleArn=arn, RoleSessionName=role_session_name, DurationSeconds=duration_seconds
    )
    role_ak = response['Credentials'].get('AccessKeyId')
    role_sk = response['Credentials'].get('SecretAccessKey')
    role_token = response['Credentials']['SessionToken']
    return AwsCredential(aws_access_key_id=role_ak, aws_secret_access_key=role_sk, aws_session_token=role_token)


def tencent_assume_role(ak, sk, arn, session_name='fetch_asset', duration_seconds=3600):
    return STSAssumeRoleCredential(ak, sk, arn, session_name, duration_seconds)



