# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.ec2 import Ec2, NatGateways, Vpc, Subnets, SecurityGroups, NetworkInterfaces


class TestEc2CpuUtilization(BaseAwsTest):

    def load_asset(self):
        return Ec2(self.cred, self.region, dbconfig=self.db_config)


class TestNatGateways(BaseAwsTest):
    def load_asset(self):
        return Vpc(self.cred, self.region, dbconfig=self.db_config)


class TestVpc(BaseAwsTest):
    def load_asset(self):
        return NatGateways(self.cred, self.region, dbconfig=self.db_config)


class TestSubnets(BaseAwsTest):
    def load_asset(self):
        return Subnets(self.cred, self.region, dbconfig=self.db_config)


class TestSecurityGroups(BaseAwsTest):
    def load_asset(self):
        return SecurityGroups(self.cred, self.region, dbconfig=self.db_config)


class TestNetworkInterfaces(BaseAwsTest):
    def load_asset(self):
        return NetworkInterfaces(self.cred, self.region, dbconfig=self.db_config)