# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.cloudwatch import Ec2CpuUtilization


class TestEc2CpuUtilization(BaseAwsTest):

    def load_asset(self):
        return Ec2CpuUtilization(self.cred, self.region, dbconfig=self.db_config)

