# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os

from asset.base import Asset
from asset.utils import aws_assume_role
from asset.schema import DbConfig

db_config = DbConfig(
    host=os.getenv('HOST'),
    port=os.getenv('PORT'),
    password=os.getenv('PASSWORD'),
    user=os.getenv('USER'),
    database=os.getenv('DATABASE'),
)

aws_arn = os.getenv('AWS_ARN')
aws_region = 'cn-northwest-1'
aws_cred = aws_assume_role(arn=aws_arn)


class BaseAwsTest:
    _asset: Asset = None
    _region = aws_region

    def __init__(self):
        self.asset = self._asset(aws_cred, region=aws_region, dbconfig=db_config)

    def test_account_id(self):
        assert self.asset.account_id is not None

    def test_paginate_all_assets(self):
        assert isinstance(self.asset.paginate_all_assets, list) == True

    def test_fetch(self):
        assert self.asset.fetch() == True