# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
from typing import List
from pydantic import BaseModel
from aliyunsdkcore.auth.credentials import RamRoleArnCredential
from tencentcloud.common.credential import STSAssumeRoleCredential


class DbConfig(BaseModel):
    host: str = os.getenv('CLOUD_ASSERT_HOST', '')
    port: int = os.getenv('CLOUD_ASSERT_PORT', 5432)
    password: str = os.getenv('CLOUD_ASSERT_PASSWORD', '')
    user: str = os.getenv('CLOUD_ASSERT_USER', '')
    database: str = os.getenv('CLOUD_ASSERT_DATABASE', '')


class AssetColumn(BaseModel):
    name: str
    type: str
    length: int = None
    kwargs: dict = {'nullable': True, 'default': None}


class TencentRole(BaseModel):
    arn: str
    session_name: str = 'fetch_asset'
    duration_seconds: int = 3600


class AliyunRole(BaseModel):
    arn: str
    session_name: str = 'fetch_asset'


class AwsRole(AliyunRole):
    duration_seconds: int = 3600


class TencentProfile(BaseModel):
    ak: str
    sk: str
    roles: List[TencentRole] = []


class AliyunProfile(BaseModel):
    ak: str
    sk: str
    roles: List[AliyunRole] = []


class AwsProfile(BaseModel):
    roles: List[AwsRole] = []


class AwsCredential(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str



