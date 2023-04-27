# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os

from asset.base import Asset
from asset.utils import aws_assume_role, tencent_assume_role, aliyun_assume_role
from asset.schema import DbConfig, HuaweiCredential


db_config = DbConfig(
    host=os.getenv('HOST'),
    port=os.getenv('PORT'),
    password=os.getenv('PASSWORD'),
    user=os.getenv('USER'),
    database=os.getenv('DATABASE')
)


class BaseAwsTest:
    arn = os.getenv('AWS_ARN')
    region = 'cn-northwest-1'
    # cred = aws_assume_role(arn=arn)
    db_config = db_config

    @property
    def asset(self):
        return self.load_asset()

    @property
    def cred(self):
        return aws_assume_role(arn=self.arn)

    def load_asset(self) -> Asset:
        pass

    def test_account_id(self):
        assert self.asset.account_id is not None

    def test_fetch(self):
        assert self.asset.fetch() == True


class BaseTencentTest(BaseAwsTest):
    arn = os.getenv('TENCENT_ARN')
    region = 'ap-shanghai'
    # cred = tencent_assume_role(ak=os.getenv('TENCENT_AK'), sk=os.getenv('TENCENT_SK'), arn=arn)

    @property
    def cred(self):
        return tencent_assume_role(ak=os.getenv('TENCENT_AK'), sk=os.getenv('TENCENT_SK'), arn=self.arn)


class BaseAliyunTest(BaseAwsTest):
    arn = os.getenv('ALIYUN_ARN')
    region = 'cn-chengdu'
    # cred = aliyun_assume_role(ak=os.getenv('ALIYUN_AK'), sk=os.getenv('ALIYUN_SK'), arn=arn)

    @property
    def cred(self):
        return aliyun_assume_role(ak=os.getenv('ALIYUN_AK'), sk=os.getenv('ALIYUN_SK'), arn=self.arn)


class BaseHuaweiTest:
    db_config = db_config
    region = 'cn-south-1'
    cred = HuaweiCredential(ak=os.getenv('HUAWEI_AK', ''), sk=os.getenv('HUAWEI_SK', ''))

    @property
    def asset(self):
        return self.load_asset()

    def load_asset(self) -> Asset:
        pass

    def test_account_id(self):
        assert self.asset.account_id is not None

    def test_fetch(self):
        assert self.asset.fetch() == True

