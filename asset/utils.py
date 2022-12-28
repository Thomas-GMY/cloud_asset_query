# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0
import re
import json

from tencentcloud.cam.v20190116 import cam_client, models

from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest
from aliyunsdkcore.client import AcsClient

from boto3 import client as aws_client

from asset.schema import AwsCredential


def to_hump_underline(string) -> str:
    return re.sub(r"(?P<key>[A-Z])", r"_\g<key>", string).lower().strip('_')


def tencent_parser_response(response, response_filed: str) -> list:
    return json.loads(response.to_json_string())[response_filed]


def aliyun_parser_response(response, response_filed: str, child_response_filed: str = None) -> list:
    if child_response_filed:
        return json.loads(response)[response_filed][child_response_filed]
    return json.loads(response)[response_filed]


def aws_parser_response(response: dict, response_filed: str) -> list:
    return response.get('response_filed')


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


def aws_assume_role(ak, sk, arn, role_session_name='fetch_asset', duration_seconds=3600) -> AwsCredential:
    response = aws_client('sts', aws_access_key_id=ak, aws_secret_access_key=sk).assume_role(
        RoleArn=arn, RoleSessionName=role_session_name, DurationSeconds=duration_seconds
    )
    role_ak = response['Credentials'].get('AccessKeyId')
    role_sk = response['Credentials'].get('SecretAccessKey')
    role_token = response['Credentials']['SessionToken']
    return AwsCredential(aws_access_key_id=role_ak, aws_secret_access_key=role_sk, aws_session_token=role_token)

