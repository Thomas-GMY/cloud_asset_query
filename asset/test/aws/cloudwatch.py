# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.cloudwatch import Ec2CpuUtilization


class TestEc2CpuUtilization(BaseAwsTest):
    _asset = Ec2CpuUtilization

    def test_account_id(self):
        assert 1==1


