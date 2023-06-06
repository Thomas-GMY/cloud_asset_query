# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import re
import json
import boto3
import datetime
import logging

from tencentcloud.cam.v20190116 import cam_client, models

from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest
from aliyunsdkcore.client import AcsClient

from huaweicloudsdkcore.sdk_response import SdkResponse

from boto3 import client as aws_client
from typing import Tuple, Union

from asset.schema import AwsCredential, STSAssumeRoleCredential, RamRoleArnCredential, HuaweiCredential


_IGNORE_ERROR_MSG = 'EntityNotExist.User.LoginProfile login policy not exists'


def retry(retry_count=5):
    """
    :param retry_count: 重试次数
    :return:
    """
    logger = logging.getLogger('cloud-asset-fetch')

    def decorator(func):
        def handler(*args, **kwargs):

            all_fail, error, response = 0, None, None
            for i in range(retry_count):
                try:
                    if i > 0:
                        logger.info(f'开始重试, 重试次数{i}')
                    response = func(*args, **kwargs)
                    break
                except Exception as e:
                    if _IGNORE_ERROR_MSG in str(e):
                        response = None
                        break

                    all_fail += 1
                    error = e
                    continue

            if all_fail == retry_count:
                logger.info('全部重试失败！')
                raise error

            return response

        return handler
    return decorator


def to_hump_underline(string) -> str:
    return re.sub(r"(?P<key>[A-Z])", r"_\g<key>", string).lower().strip('_')


def register_assets(cloud_provider):
    import importlib
    from asset.asset_register import cloud_providers

    importlib.import_module(f'asset.{cloud_provider}')
    return getattr(cloud_providers, cloud_provider)


def tencent_parser_response(response, response_filed: str) -> Union[list, dict]:
    return json.loads(response.to_json_string())[response_filed]


def aliyun_parser_response(response, response_filed: str, child_response_filed: str = None) -> list:
    if child_response_filed:
        return json.loads(response)[response_filed][child_response_filed]
    return json.loads(response)[response_filed]


def aws_parser_response(
        response: dict, response_filed: str, child_response_filed: str = None) -> Tuple[Union[list, str, dict], str]:
    assets = response.get(response_filed)
    next_token = response.get('NextToken') or response.get('NextMarker')
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

    if isinstance(assets, dict):
        assets = [assets]

    return assets, next_token


def huawei_parser_response(response: dict, response_filed: str) -> list:
    return response.get(response_filed)


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
        elif isinstance(value, datetime.datetime):
            _value_list = value.strftime('%Y-%m-%d %H:%M:%S')
        else:
            _value_list.append(_value)
    return _value_list


def recursive_list_huawei_assets(assets: list):
    _assets = []
    for index in range(len(assets)):
        _asset = assets[index]
        if isinstance(_asset, SdkResponse):
            _assets.append(_asset.to_json_object())


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


def get_huawei_account_id(cred: HuaweiCredential):
    from huaweicloudsdkcore.auth.credentials import GlobalCredentials
    from huaweicloudsdkiam.v3.region.iam_region import IamRegion
    from huaweicloudsdkcore.exceptions import exceptions
    from huaweicloudsdkiam.v3.iam_client import IamClient
    from huaweicloudsdkiam.v3.model import KeystoneListAuthDomainsRequest

    credentials = GlobalCredentials(cred.ak, cred.sk)

    client = IamClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(IamRegion.value_of("cn-south-1")) \
        .build()

    try:
        request = KeystoneListAuthDomainsRequest()
        response = client.keystone_list_auth_domains(request).to_dict()
        domains = response.get('domains', [])
        if not domains:
            raise Exception('not find domain id')
        return domains[0].get('id')
    except exceptions.ClientRequestException as e:
        raise e


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


def aliyun_assume_role(ak, sk, arn, session_name='fetch_asset'):
    return RamRoleArnCredential(ak, sk, arn, session_name)



